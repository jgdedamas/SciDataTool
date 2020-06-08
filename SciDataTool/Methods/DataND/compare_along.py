# -*- coding: utf-8 -*-
from SciDataTool.Functions.interpolations import get_common_base, get_interpolation
from numpy import squeeze, array


def compare_along(self, *args, data_list=[], unit="SI", is_norm=False):
    """Returns the ndarrays of both fields interpolated in the same axes, using conversions and symmetries if needed.
    Parameters
    ----------
    self: Data
        a Data object
    *args: list of strings
        List of axes requested by the user, their units and values (optional)
    data_list: list
        list of Data objects to compare
    unit: str
        Unit requested by the user ("SI" by default)
    is_norm: bool
        Boolean indicating if the field must be normalized (False by default)
    Returns
    -------
    list of 1Darray of axis values, ndarrays of fields
    """
    if data_list == []:
        return self.get_along(args, unit=unit, is_norm=is_norm)
    else:
        # Extract requested axes + field values
        results = self.get_along(args, unit=unit, is_norm=is_norm)
        values = results.pop(self.symbol)
        axes = results
        data_axis_values = []
        data_values = []
        return_dict = {}
        for data in data_list:
            results = data.get_along(args, unit=unit, is_norm=is_norm)
            data_values.append(results.pop(data.symbol))
            data_axis_values.append(results)
        # Get the common bases
        common_axis_values = {}
        for axis in axes.keys():
            common_axis_values[axis] = axes[axis]
            for i, data in enumerate(data_list):
                common_axis_values[axis] = get_common_base(
                    common_axis_values[axis], data_axis_values[i][axis]
                )
            # Interpolate over common axis values
            values = get_interpolation(values, axes[axis], common_axis_values[axis])
            for i, data in enumerate(data_list):
                data_values[i] = get_interpolation(
                    data_values[i],
                    data_axis_values[i][axis],
                    common_axis_values[axis],
                )
            return_dict[axis] = common_axis_values[axis]
        # Return axis and values
        return_dict[self.symbol + "_ref"] = values
        for i, data in enumerate(data_list):
            return_dict[data.symbol + "_" + str(i)] = data_values[i]
        return return_dict
