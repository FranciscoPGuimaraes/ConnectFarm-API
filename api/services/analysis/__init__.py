from .health.health_history import analyze_health_history
from .health.health_not_recovered import get_not_recovered_cows

from .calves.calves_ratio import calculate_weaned_calves_ratio
from .calves.calves_time import analyze_weaning_time
from .calves.calves_preditions import get_calf_data, project_growth

from .vaccines.vaccines_coverage import calculate_vaccine_coverage
from .vaccines.vaccines_quarter import get_vaccinations_by_quarter

from .weight.weight_variation import analyze_weight_variation
from .weight.weight_montly import analyze_weight_variation_month
from .weight.weight_grid import get_cattle_weights

from .financial.financials_per_cow import analyze_financials_per_cow
from .financial.financial_current import analyze_financials_current
from .financial.financial_predict import analyze_financials_prediction

from .location.location_data import get_locations
