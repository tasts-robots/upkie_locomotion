#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2022 Stéphane Caron
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

from typing import Tuple

import gin
import numpy as np

from utils.clamp import clamp_abs


@gin.configurable
def forward_kinematics(
    q_hip: float, q_knee: float, limb_length: float
) -> float:
    """
    Compute forward kinematics for a single leg.

    Args:
        q_hip: Angle of the hip joint, in radians.
        q_knee: Angle of the knee joint, in radians.
        limb_length: (Model) Length of both links of the leg.

    Returns:
        Crouch height (positive, zero for extended legs) in meters.

    The derivation of this function is documented in `Kinematics of a
    symmetric leg`_.

    .. _`Kinematics of a symmetric leg`:
        https://scaron.info/blog/kinematics-of-a-symmetric-leg.html
    """
    height = limb_length * (np.cos(q_hip) + np.cos(q_hip + q_knee))
    leg_length = 2.0 * limb_length
    crouch_height = leg_length - height
    return crouch_height


@gin.configurable
def inverse_kinematics(
    crouch_height: float,
    crouch_velocity: float,
    limb_length: float,
    velocity_limit: float,
) -> Tuple[Tuple[float, float], Tuple[float, float]]:
    """
    Solve inverse kinematics for a single leg.

    Args:
        crouch_height: Crouch height (positive, zero for extended legs) in
            meters.
        crouch_velocity: Time derivative of the crouch, in m / s.
        limb_length: (Model) Length of both links of the leg.
        velocity_limit: (Model) Maximum joint velocity in rad / s.

    Returns:
        ===========  =========================================================
        ``q_hip``     Angle of the hip joint in radians.
        ``q_knee``    Angle of the knee joint in radians.
        ``v_hip``     Angular velocity for the hip joint in rad / s.
        ``v_knee``    Angular velocity for the knee joint in rad / s.
        ===========  =========================================================

    The derivation of this function is documented in `Kinematics of a symmetric
    leg`_. We replaced the total height :math:`h` by the crouch height :math:`c
    = 2 * \\ell - h`.

    .. _`Kinematics of a symmetric leg`:
        https://scaron.info/blog/kinematics-of-a-symmetric-leg.html
    """
    leg_length = 2.0 * limb_length
    assert 0.0 <= crouch_height < leg_length, (
        f"Invalid crouch height: {crouch_height} [m]; "
        "leg is under- or over-extended"
    )

    q_hip = clamp_abs(
        np.arccos(1.0 - crouch_height / leg_length),
        0.5 * np.pi,
    )

    # Time-derivative of the formula for q_hip
    squared_denom = crouch_height * (2.0 * leg_length - crouch_height)
    v_hip = (
        clamp_abs(
            crouch_velocity / np.sqrt(squared_denom),
            velocity_limit,
        )
        if squared_denom > 1e-10
        else np.sign(crouch_velocity) * velocity_limit
    )

    q_knee = clamp_abs(-2.0 * q_hip, np.pi)
    v_knee = clamp_abs(-2.0 * v_hip, velocity_limit)
    return (q_hip, q_knee), (v_hip, v_knee)
