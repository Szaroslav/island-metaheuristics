import dataclasses


@dataclasses.dataclass
class RunAlgorithmParams:
    island_count: int
    number_of_emigrants: int
    migration_interval: int
    dda: str
    tta: str
    series_number: int
    topology: str
    strategy: str
    # nowe, opcjonalne parametry dla ScaleFreeTopology:
    m0: int = None
    m:  int = None
