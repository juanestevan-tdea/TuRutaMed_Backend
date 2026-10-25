import pytest

from app.database_seeder import (
    SITVA_ROUTES,
    _normalizar_ruta,
    _validar_catalogo,
    seed_rutas_if_empty,
)


def _ruta_base(**overrides):
    ruta = {
        "nombre_ruta": "Ruta de prueba",
        "tipo_transporte": "Bus",
        "origen": "A",
        "destino": "B",
        "tiempo_estimado_minutos": 10,
        "coordenadas": [-75.56, 6.25],
        "paraderos": [
            {"nombre_paradero": "A", "coordenadas": [-75.56, 6.25], "orden": 1},
            {"nombre_paradero": "B", "coordenadas": [-75.57, 6.26], "orden": 2},
        ],
    }
    ruta.update(overrides)
    return ruta


def test_catalogo_sitva_tiene_nueve_rutas_unicas():
    rutas = [_normalizar_ruta(ruta) for ruta in SITVA_ROUTES]
    _validar_catalogo(rutas)
    assert len(rutas) == 9


def test_catalogo_no_mezcla_esquemas_de_coordenadas():
    for ruta in SITVA_ROUTES:
        normalizada = _normalizar_ruta(ruta)
        assert isinstance(normalizada["coordenadas"], list)
        assert len(normalizada["coordenadas"]) == 2
        for paradero in normalizada["paraderos"]:
            assert set(paradero).isdisjoint({"latitud", "longitud"})
            assert isinstance(paradero["coordenadas"], list)
            assert len(paradero["coordenadas"]) == 2


def test_normalizacion_migra_latitud_longitud_a_coordenadas():
    ruta = _ruta_base(
        paraderos=[
            {"nombre_paradero": "A", "latitud": 6.25, "longitud": -75.56, "orden": 1},
            {"nombre_paradero": "B", "latitud": 6.26, "longitud": -75.57, "orden": 2},
        ],
    )
    ruta.pop("coordenadas")

    normalizada = _normalizar_ruta(ruta)

    assert normalizada["paraderos"][0]["coordenadas"] == [-75.56, 6.25]
    assert "latitud" not in normalizada["paraderos"][0]
    assert "longitud" not in normalizada["paraderos"][0]
    assert normalizada["coordenadas"] == [-75.56, 6.25]


def test_normalizacion_rechaza_coordenadas_fuera_de_rango():
    ruta = _ruta_base(
        paraderos=[
            {"nombre_paradero": "A", "coordenadas": [-75.56, 96.25], "orden": 1},
        ]
    )

    with pytest.raises(ValueError, match="latitud fuera de rango"):
        _normalizar_ruta(ruta)


def test_normalizacion_rechaza_ruta_sin_paraderos():
    with pytest.raises(ValueError, match="no tiene paraderos"):
        _normalizar_ruta(_ruta_base(paraderos=[]))


class _FakeCollection:
    def __init__(self, docs=None):
        self.docs = {doc["nombre_ruta"]: doc for doc in (docs or [])}
        self.deleted_count = 0
        self.indexes = []

    def delete_many(self, _filtro):
        self.deleted_count = len(self.docs)
        self.docs.clear()
        return type("Resultado", (), {"deleted_count": self.deleted_count})()

    def create_index(self, llave, name=None):
        self.indexes.append((llave, name))

    def replace_one(self, filtro, documento, upsert=False):
        assert upsert is True
        self.docs[filtro["nombre_ruta"]] = documento

    def count_documents(self, _filtro):
        return len(self.docs)


class _FakeDB:
    def __init__(self, docs=None):
        self.collection = _FakeCollection(docs)

    def __getitem__(self, _nombre):
        return self.collection


def test_seed_force_borra_y_deja_solo_el_catalogo():
    db = _FakeDB(docs=[{"nombre_ruta": "Vieja"}, {"nombre_ruta": "Otra vieja"}])

    total = seed_rutas_if_empty(db, force=True)

    assert total == 9
    assert len(db.collection.docs) == 9
    assert db.collection.deleted_count == 2
    llaves = [llave for llave, _ in db.collection.indexes]
    assert ("paraderos.coordenadas", "2dsphere") in llaves[0]


def test_seed_sin_force_conserva_rutas_personalizadas():
    db = _FakeDB(docs=[{"nombre_ruta": "Ruta propia"}])

    seed_rutas_if_empty(db, force=False)

    assert "Ruta propia" in db.collection.docs
    assert len(db.collection.docs) == 10
