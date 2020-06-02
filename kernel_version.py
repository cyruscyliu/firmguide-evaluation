import re


def find_kernel_version_in_string(string):
    """Find which Linux kernel version the image belongs to.

    Args:
        string(str): String from the image.

    Returns:
        str: The Linux kernel version the image may belongs to.
    """
    patterns = [r'Linux-(\d+\.\d+\.\d+)', r'.*\((\d+\.\d+\.\d+)\)', r'[lL]inux version ([1-5]+\.\d+\.\d+).*']

    kernel_version = None
    for pattern in patterns:
        kernel_version = re.search(pattern, string)
        if kernel_version is not None:
            kernel_version = kernel_version.groups()[0]
            break

    return kernel_version


def find_kernel_version_in_strings(strings):
    """Find which Linux kernel version the image belongs to.

    Args:
        strings(list): Strings from the image.

    Returns:
        str: The Linux kernel version the image may belongs to.
    """
    for string in strings:
        kernel_version = find_kernel_version_in_string(string)
        if kernel_version is not None:
            return kernel_version


if __name__ == '__main__':
    print(find_kernel_version_in_string('[1] Linux-3.3.8,'))
    print(find_kernel_version_in_string('Description:  ARM OpenWrt Linux-3.18.20'))
    print(find_kernel_version_in_string('linux version 3.18.20'))
    print(find_kernel_version_in_string('Linux version 3.18.20'))
