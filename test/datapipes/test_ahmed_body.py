# SPDX-FileCopyrightText: Copyright (c) 2023 - 2024 NVIDIA CORPORATION & AFFILIATES.
# SPDX-FileCopyrightText: All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
import torch
from pytest_utils import import_or_fail

from . import common

Tensor = torch.Tensor


@pytest.fixture
def data_dir(nfs_data_dir):
    return nfs_data_dir.joinpath("datasets/ahmed_body")


@import_or_fail(["vtk", "pyvista", "dgl"])
@pytest.mark.parametrize("device", ["cuda:0", "cpu"])
def test_ahmed_body_constructor(data_dir, device, pytestconfig):
    from physicsnemo.datapipes.gnn.ahmed_body_dataset import AhmedBodyDataset

    # construct dataset
    dataset = AhmedBodyDataset(
        data_dir=data_dir,
        split="train",
        num_samples=2,
        compute_drag=True,
    )

    # iterate datapipe is iterable
    common.check_datapipe_iterable(dataset)

    # check for failure from invalid dir
    try:
        # init dataset with empty path
        # if dataset throws an IO error then this should pass
        dataset = AhmedBodyDataset(
            data_dir="/null_path",
            split="train",
            num_samples=2,
            compute_drag=True,
        )
        raise IOError("Failed to raise error given null data path")
    except IOError:
        pass

    # check invalid split
    try:
        # if dataset throws an IO error then this should pass
        dataset = AhmedBodyDataset(
            data_dir=data_dir,
            invar_keys=[
                "pos",
                "normals",
                "velocity",
                "reynolds_number",
                "length",
                "width",
                "height",
                "ground_clearance",
                "slant_angle",
                "fillet_radius",
            ],
            split="valid",
            num_samples=2,
            compute_drag=True,
        )
        raise IOError("Failed to raise error given invalid split")
    except IOError:
        pass
