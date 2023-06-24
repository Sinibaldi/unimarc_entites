# coding: utf-8

import streamlit as st
import pandas as pd
from lxml import etree

ns = {"m": "http://www.loc.gov/MARC21/slim"}

def extract_files(fnames_list):
    stats_entities = {}
    for f in fnames_list:
        stats_entities[f] = extract_file(fnames_list[f], f)
    st.write(stats_entities)
    st.line_chart(stats_entities.values())

def extract_file(fname, entity_type):
    tree = etree.parse(fname)
    nb_entities = 0
    for record in tree.xpath("//m:record", namespaces=ns):
        nb_entities += 1
    return nb_entities



if __name__ == "__main__":
    fnames = {"item": "UMH_Items.xml",
              "manif": "UMB_Manifestations.xml",
              "o_e": "UMA_Oeuvres_Expressions.xml",
              "autres": "UMA_Autres_Entites_Liees.xml"}
    extract_files(fnames)