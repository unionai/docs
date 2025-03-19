import os
from typing import Dict, List

from lib.generate.classes import generate_class_index, generate_classes
from lib.generate.hugo import set_variants, set_version, write_front_matter
from lib.generate.packages import (
    generate_package_folders,
    generate_package_index,
)
from lib.ptypes import ParsedInfo

type PackageTree = Dict[str, List[str]]


def generate_home(
    title: str,
    source: ParsedInfo,
    include: List[str],
    doc_level: int,
    pkg_root: str,
    output_folder: str,
):
    with open(os.path.join(output_folder, "_index.md"), "w") as output:
        write_front_matter(title, output)

        output.write(f"# {title}\n\n")

        for inc in include:
            with open(inc, "r") as f:
                output.write(f.read())
                output.write("\n\n")

def generate_site(
    title: str,
    source: ParsedInfo,
    include: List[str],
    doc_level: int,
    output_folder: str,
    variants: List[str],
    flatten: bool,
    ignore_types: List[str],
):
    set_variants(variants)
    set_version(source["version"])

    if not os.path.isdir(output_folder):
        os.mkdir(output_folder)

    pkg_root = os.path.join(output_folder, "packages")
    if not os.path.isdir(pkg_root):
        os.mkdir(pkg_root)

    # Generate site
    generate_home(
        title=title,
        source=source,
        include=include,
        doc_level=doc_level,
        output_folder=output_folder,
        pkg_root=pkg_root,
    )

    generate_package_index(
        packages=source["packages"], classes=source["classes"], pkg_root=pkg_root
    )
    generate_class_index(
        classes=source["classes"], output_folder=output_folder, pkg_root=pkg_root, flatten=flatten, ignore_types=ignore_types
    )

    generate_package_folders(
        packages=source["packages"],
        classes=source["classes"],
        pkg_root=pkg_root,
        flatten=flatten,
        ignore_types=ignore_types,
    )

    if flatten:
        pass
    else:
        generate_classes(classes=source["classes"], pkg_root=pkg_root, ignore_types=ignore_types)
