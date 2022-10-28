from copy import deepcopy

import pytest

from rook_client.stone import stonecluster as cc


def test_omit():
    cv = cc.StoneVersion()
    with pytest.raises(AttributeError):
        cv.allowUnsupported

    assert not hasattr(cv, 'allowUnsupported')
