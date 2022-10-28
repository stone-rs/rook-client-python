from os.path import expanduser, dirname, realpath

import yaml
import pytest

import rook_client
from rook_client.cassandra.cluster import Cluster as CassandraCluster
from rook_client.stone.stonecluster import StoneCluster
from rook_client.stone.stonefilesystem import StoneFilesystem
from rook_client.stone.stonenfs import StoneNFS
from rook_client.stone.stoneobjectstore import StoneObjectStore
from rook_client.stone.stoneblockpool import StoneBlockPool


def _load_example(crd_base, what):
    with open(expanduser('{crd_base}/{what}').format(crd_base=crd_base, what=what)) as f:
        return f.read()


@pytest.mark.parametrize(
    "strict,cls,filename",
    [
        (True, StoneCluster, "stone/cluster-external.yaml"),
        (True, StoneCluster, "stone/cluster-on-pvc.yaml"),
        (True, StoneCluster, "stone/cluster.yaml"),
        (True, StoneFilesystem, "stone/filesystem-ec.yaml"),
        (True, StoneFilesystem, "stone/filesystem-test.yaml"),
        (True, StoneFilesystem, "stone/filesystem.yaml"),
        (True, StoneObjectStore, "stone/object-ec.yaml"),
        (True, StoneObjectStore, "stone/object-openshift.yaml"),
        (True, StoneObjectStore, "stone/object-test.yaml"),
        (True, StoneObjectStore, "stone/object.yaml"),
        (True, StoneNFS, "stone/nfs.yaml"),
        (True, StoneBlockPool, "stone/pool.yaml"),
        (True, StoneBlockPool, "stone/pool-ec.yaml"),
        (True, StoneBlockPool, "stone/pool-test.yaml"),

        # schema invalid:
        # (False, CassandraCluster, "cassandra/cluster.yaml"),
    ],
)
def test_exact_match(strict, cls, filename, crd_base):
    crds = yaml.safe_load_all(_load_example(crd_base, filename))
    rook_client.STRICT = strict
    [crd] = [e for e in crds if e.get('kind', '') == cls.__name__]

    c = cls.from_json(crd)
    assert crd == c.to_json()




