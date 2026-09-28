"""Raft Snapshot Compaction and Install Engine.
100% Python Standard Library.
"""

class RaftSnapshotManager:
    """Raft state machine snapshotting and log compaction."""
    def __init__(self):
        self.log = []
        self.last_included_index = 0
        self.last_included_term = 0
        self.snapshot_state = {}

    def take_snapshot(self, up_to_index, state_dict):
        if up_to_index <= self.last_included_index or up_to_index > len(self.log) + self.last_included_index:
            return False
        local_idx = up_to_index - self.last_included_index - 1
        self.last_included_term = self.log[local_idx][0]
        self.last_included_index = up_to_index
        self.snapshot_state = dict(state_dict)
        self.log = self.log[local_idx + 1:]
        return True

    def install_snapshot(self, last_index, last_term, state_dict):
        self.last_included_index = last_index
        self.last_included_term = last_term
        self.snapshot_state = dict(state_dict)
        self.log = []
