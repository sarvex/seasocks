#!/usr/bin/env python

import os, os.path, sys, argparse

SOURCE_TEMPLATE = """
#include "internal/Embedded.h"

#include <string>
#include <unordered_map>

namespace {
%s

    const std::unordered_map<std::string, EmbeddedContent> embedded = {
%s
    };

}  // namespace

const EmbeddedContent* findEmbeddedContent(const std::string& name) {
    const auto found = embedded.find(name);
    if (found == embedded.end()) {
        return nullptr;
    }
    return &found->second;
}\n
"""

MAX_SLICE = 16

def as_byte(data):
    return ord(data) if sys.version_info < (3,) else data


def parse_arguments():
    parser = argparse.ArgumentParser(description="Embedded content generator")
    parser.add_argument('--output', '-o', action='store', dest='output_file', type=str, help='Output File', required=True)
    parser.add_argument('--file', '-f', action='store', nargs='+', dest='input_file', type=str, help='Output File', required=True)
    return parser.parse_args()


def create_file_byte(name, file_bytes):
    output = ['    const char %s[%d] = {\n' % (name, len(file_bytes) + 1)]
    output.extend(
        "        "
        + "".join(
            "'\\x{:02x}',".format(as_byte(x))
            for x in file_bytes[start : start + MAX_SLICE]
        )
        + "\n"
        for start in range(0, len(file_bytes), MAX_SLICE)
    )
    output.extend(('        0x00,\n', '    };\n'))
    return ''.join(output)


def create_file_info(file_list):
    output = [
        '        {"/%s", { %s, %d }},\n' % (base, name, length)
        for name, base, length in file_list
    ]
    return ''.join(output)


def main():
    args = parse_arguments()

    files = []
    file_byte_entries = []

    for index, file_name in enumerate(args.input_file, start=1):
        with open(file_name, 'rb') as f:
            file_bytes = f.read()
        name = "fileData%d" % index
        files.append((name, os.path.basename(file_name), len(file_bytes)))
        file_byte_entries.append(create_file_byte(name, file_bytes))

    with open(args.output_file, 'w') as output_file:
        output_file.write(SOURCE_TEMPLATE % (''.join(file_byte_entries), create_file_info(files)))


if __name__ == '__main__':
    main()
