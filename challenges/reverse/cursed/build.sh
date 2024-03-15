#!/bin/bash

mlton -codegen c -link-opt '-static' cursed.sml
