
import ray

from islands_desync.geneticAlgorithm.migrations.ray_migration_pipeline import \
    RayMigrationPipeline
from islands_desync.geneticAlgorithm.run_hpc.create_algorithm_hpc import \
    create_algorithm_hpc
from islands_desync.geneticAlgorithm.run_hpc.run_algorithm_params import \
    RunAlgorithmParams
from islands_desync.islands.core.Emigration import Emigration


@ray.remote
class Computation:
    def __init__(
        self,
        island,
        n: int,
        islands,
        select_algorithm,
        algorithm_params: RunAlgorithmParams,
    ):
        self.island = island
        self.n: int = n

        self.emigration = Emigration.remote(islands, select_algorithm)
        self.migration = RayMigrationPipeline(island, self.emigration)

        self.algorithm = create_algorithm_hpc(
            n, self.migration, algorithm_params
        )

    def start(self):

        self.algorithm.run()
        result = self.algorithm.get_result()

        calculations = {
            "island": self.n,
            "iterations": self.algorithm.step_num,
            "time": self.migration.run_time(),
            "ips": self.algorithm.step_num / self.migration.run_time(),
            "start": self.migration.start,
            "end": self.migration.end
        }

        print(f"\nIsland: {self.n} Fitness: {result.objectives[0]}")

        return calculations
