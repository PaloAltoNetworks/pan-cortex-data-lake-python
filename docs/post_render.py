#!/usr/bin/env python
# -*- coding: utf-8 -*-


from editfrontmatter import EditFrontMatter
import os
import glob


def main():
    template_str = "".join(open(os.path.abspath("docs/template.j2"), "r").readlines())
    md_files = glob.glob("./docs/**/*.md", recursive=True)
    for path in md_files:
        github_base_url = "https://github.com/PaloAltoNetworks/pan-cortex-data-lake-python/blob/master/pan_cortex_data_lake"
        github_file_path = path.split("/reference")[1].replace(".md", ".py")
        custom_edit_url = f"{github_base_url}{github_file_path}"  # noqa: E999
        proc = EditFrontMatter(file_path=path, template_str=template_str)
        proc.run({"custom_edit_url": custom_edit_url})
        proc.writeFile(path)


if __name__ == "__main__":
    main()
