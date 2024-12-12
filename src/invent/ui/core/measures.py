"""
The core units of measurement used by UI properties in the Invent framework.

Based on original pre-COVID work by [Nicholas H.Tollervey.](https://ntoll.org/)

Copyright (c) 2024 Invent contributors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# The names of sizes.

#: The very smallest size, as a t-shirt size.
EXTRA_SMALL = "XS"
#: A small size, as a t-shirt size.
SMALL = "S"
#: A medium size, as a t-shirt size.
MEDIUM = "M"
#: A large size, as a t-shirt size.
LARGE = "L"
#: The very largest size, as a t-shirt size.
EXTRA_LARGE = "XL"

#: T-shirt sizes for widths/gaps.
TSHIRT_SIZES = (
    None,
    EXTRA_SMALL,
    SMALL,
    MEDIUM,
    LARGE,
    EXTRA_LARGE,
)

# Size values in pixels.

#: Extra small, as a pixel value.
XS_SIZE = "1px"
#: Small, as a pixel value.
S_SIZE = "2px"
#: Medium, as a pixel value.
M_SIZE = "4px"
#: Large, as a pixel value.
L_SIZE = "8px"
#: Extra large, as a pixel value.
XL_SIZE = "16px"

#: T-shirt sizes for gaps between things.
GAP_SIZES = {
    EXTRA_SMALL: XS_SIZE,
    SMALL: S_SIZE,
    MEDIUM: M_SIZE,
    LARGE: L_SIZE,
    EXTRA_LARGE: XL_SIZE,
}

#: Choices for the distribution of child components within a container.
COMPONENT_DISTRIBUTION = [
    "start",
    "center",
    "end",
    "stretch",
    "space-between",
    "space-around",
    "space-evenly",
]
