# -*- python -*-
#
# Copyright 2022 Stéphane Caron

load("//tools/lint:lint.bzl", "add_lint_tests")

package(default_visibility = ["//visibility:public"])

filegroup(
    name = "config",
    srcs = glob([
        "*.gin",
        "*.yaml",
    ]),
)

py_library(
    name = "kinematics",
    srcs = [
        "kinematics.py",
    ],
    deps = [
        "//utils:clamp",
        "@pip_upkie_locomotion//pypi__gin_config",
        "@pip_upkie_locomotion//pypi__numpy",
    ],
)

py_library(
    name = "wheel_balancer",
    srcs = [
        "wheel_balancer.py",
    ],
    deps = [
        "//utils:clamp",
        "//utils:filters",
        "//utils:imu",
        "@pip_upkie_locomotion//pypi__gin_config",
        "@pip_upkie_locomotion//pypi__numpy",
    ],
)

py_library(
    name = "whole_body_controller",
    srcs = [
        "whole_body_controller.py",
    ],
    deps = [
        ":kinematics",
        ":wheel_balancer",
        "@pip_upkie_locomotion//pypi__gin_config",
        "@pip_upkie_locomotion//pypi__numpy",
        "@pip_upkie_locomotion//pypi__upkie_description",
    ],
)

py_binary(
    name = "blue_balancer",
    srcs = [
        "main.py",
    ],
    main = "main.py",
    data = [
        ":config",
    ],
    deps = [
        "//utils:realtime",
        ":whole_body_controller",
        "@pip_upkie_locomotion//pypi__aiorate",
        "@pip_upkie_locomotion//pypi__gin_config",
        "@pip_upkie_locomotion//pypi__pyyaml",
        "@vulp//spine:python",
    ],
)

py_binary(
    name = "bullet",
    srcs = [
        "bullet.py",
    ],
    main = "bullet.py",
    data = [
        ":config",
        "//spines:bullet",
    ],
    deps = [
        ":whole_body_controller",
        "@pip_upkie_locomotion//pypi__aiorate",
        "@pip_upkie_locomotion//pypi__gin_config",
        "@pip_upkie_locomotion//pypi__pyyaml",
        "@rules_python//python/runfiles",
        "@vulp//spine:python",
    ],
)

add_lint_tests(enable_clang_format_lint = True)
