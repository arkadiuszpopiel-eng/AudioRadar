import numpy as np

from ml.training import RecordingController
from ml.training.session_manager import SessionManager


def test_recording_state_machine(tmp_path):
    manager = SessionManager(base_path=tmp_path)
    controller = RecordingController(session_manager=manager)

    assert controller.start_recording()
    controller.feed_audio(np.zeros((512,)))
    controller.add_label("footstep")
    session = controller.stop_recording()
    assert session is not None

    controller.discard_recording()
    assert controller.last_session is None
