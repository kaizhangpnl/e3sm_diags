# Running the software with the API:
#    python all_sets.py -d all_sets.py
from e3sm_diags.parameter.area_mean_time_series_parameter import (
    AreaMeanTimeSeriesParameter,
)
from e3sm_diags.parameter.core_parameter import CoreParameter
from e3sm_diags.parameter.enso_diags_parameter import EnsoDiagsParameter
from e3sm_diags.parameter.meridional_mean_2d_parameter import MeridionalMean2dParameter
from e3sm_diags.parameter.zonal_mean_2d_parameter import ZonalMean2dParameter
from e3sm_diags.run import Run

run_object = Run()
param = CoreParameter()
ts_param = AreaMeanTimeSeriesParameter()

m2d_param = MeridionalMean2dParameter()
m2d_param.plevs = [
    200.0,
    500.0,
]
z2d_param = ZonalMean2dParameter()
z2d_param.plevs = [
    200.0,
    300.0,
]

enso_param = EnsoDiagsParameter()
enso_param.test_name = "e3sm_v1"

run_object.run_diags([param, ts_param, m2d_param, z2d_param, enso_param])
