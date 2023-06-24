# coding: utf-8

import streamlit as st
import pandas as pd

import os
from Record import construct_indexation
from generate_records import generate_dict_entities
from generate_results import search, display_html_results, delete_html_results


def launch_app():
    dict_entities = generate_dict_entities("UMA_Oeuvres_Expressions.xml", "UMB_Manifestations.xml",
                                       "UMH_Items.xml", "UMA_Autres_Entites_Liees.xml")
    oeuvres = [dict_entities[o] for o in dict_entities if dict_entities[o].type == "o"]
    expressions = [dict_entities[e] for e in dict_entities if dict_entities[e].type == "e"]
    
    # En-tête
    display_header()

    form(dict_entities, oeuvres, expressions)


def display_header():
    st.header("Moteur de recherche", help="Afficher des listes d'oeuvres ou d'expressions")


def form(dict_entities, oeuvres, expressions):
    kw_search = st.text_input("Chercher dans la base : ")

    results_o = search(kw_search, oeuvres, dict_entities, "all")
    results_e = search(kw_search, expressions, dict_entities, "all")

    st.text(f"Nombre de résultats : {str(len(results_o))} oeuvre(s) - {str(len(results_e))} expression(s)")
    st_display_html_results(results_o, dict_entities, kw_search, "o")
    # display_html_results(results_e, dict_entities, kw_search, "e")


def st_display_html_results(dict_results, dict_entities, query, type_entity):
    # A partir d'un lot de notices d'oeuvres comme résultats d'une recherche
    # cette fonction génère 
    #       une page "results/short_results.html"  avec la liste des résultats (abrégés)
    #       et une page "results/full_results_0.html" qui pour chaque résultat génère une page HTML numérotée

    short_html = st_generate_short_results_html(dict_results, dict_entities, query, type_entity) # renvoie le code HTML
    # full_html = generate_full_results_html(dict_results, dict_entities, query, type_entity)   # renvoie une liste de code HTML

def st_generate_short_results_html(dict_results, dict_entities, query, type_entity):
    # st.write(dict_results)
    i = 1
    df = {}
    labels = []
    auteurs = []
    expressions = []
    manifs = []
    for result in dict_results:
        short_result = st_generate_short_result(result, dict_results[result], i)
        label = dict_results[result].label
        link = f'[{label}](results/full_results_{result}.html)'
        auteur = " ; ".join(dict_results[result].resp.keys())
        expression = " ; ".join([dict_results[result].toExpressions[idexpr] for idexpr in dict_results[result].toExpressions])
        expression = " ; ".join([idexpr for idexpr in dict_results[result].toExpressions])
        manif = " ; ".join([dict_results[result].toManifs[idmanif] for idmanif in dict_results[result].toManifs])
        manif = " ; ".join([idmanif for idmanif in dict_results[result].toManifs])
        df[result] = {"Label": st.markdown(link), "Auteurs": auteur, 
                      "Expressions": expression, "Manifestations": manif}

        # st.text(short_result)
        i += 1
    df = pd.DataFrame(df)
    st.table(df.transpose())
    link = '[Notice 1](results/full_results_UMLRM0001.html)'
    st.markdown(link, unsafe_allow_html=True)
    
def st_generate_short_result(entityid, entity, i):
    line = f"{str(i)}. {entity.label}"
    return line


if __name__ == "__main__":
    launch_app()