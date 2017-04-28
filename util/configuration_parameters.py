""" configuration """

import copy
from .params import feature_names, param_grid

def _create_configurations(idx, configurations):
    if idx >= 0:
        curr_feature = feature_names[idx]
        options = param_grid[curr_feature]

        if idx == len(feature_names) -1:
            for opt in options:
                configurations.append({
                    curr_feature: opt
                })
        else:
            temp_configs = []
            for opt in options:
                for conf in configurations:
                    curr_config = copy.deepcopy(conf)
                    curr_config[curr_feature] = opt
                    temp_configs.append(curr_config)

            configurations = temp_configs

        idx = idx-1
        return _create_configurations(idx, configurations)
    else:
        return configurations

def get_configurations():
    """ configurations """
    configurations = _create_configurations(len(feature_names)-1, [])

    return configurations
