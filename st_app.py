# coding: utf-8

import streamlit as st
import streamlit.components.v1 as components
import webbrowser
import pandas as pd
from lxml import etree

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

    short_html = st_generate_short_results_html(dict_results, dict_entities, query, type_entity, "list") # renvoie le code HTML
    # full_html = generate_full_results_html(dict_results, dict_entities, query, type_entity)   # renvoie une liste de code HTML

def st_generate_short_results_html(dict_results, dict_entities, query, type_entity, format="table"):
    # st.write(dict_results)
    format = "table"
    i = 1
    df = {}
    labels = []
    auteurs = []
    expressions = []
    manifs = []
    for result in dict_results:
        link = f'results/full_results_{result}.html'
        link = f"https://htmlpreview.github.io/?https://raw.githubusercontent.com/Lully/metadata_notebooks/recherche/UnimarcLRM/results/full_results_{result}.html"
        if format == "table":        
            label = dict_results[result].label
            auteur = " ; ".join(dict_results[result].resp.keys())
            expression = " ; ".join([dict_results[result].toExpressions[idexpr] for idexpr in dict_results[result].toExpressions])
            expression = " ; ".join([idexpr for idexpr in dict_results[result].toExpressions])
            manif = " ; ".join([dict_results[result].toManifs[idmanif] for idmanif in dict_results[result].toManifs])
            manif = " ; ".join([idmanif for idmanif in dict_results[result].toManifs])
            df[result] = {"id": result, "label": make_clickable(label, link), "Auteurs": auteur, 
                        "Expressions": expression, "Manifestations": manif}
        else:
            short_result = st_generate_short_result(result, dict_results[result], i)
            st.text(short_result)
            if st.button('Afficher la notice', key=result):
                    webbrowser.open_new_tab(link)
                # if st.button('Replier la notice', key=f"{result}-repli"):
                #    pass
                # HtmlFile = open(link, 'r', encoding='utf-8')
                # source_code = HtmlFile.read() 
                # components.html(source_code, height=1200)
        i += 1
    if format == "table":
        df = pd.DataFrame(df)
        df = df.transpose()
        # df = df.to_html(escape=False)
        # st.markdown(df.to_html(render_links=True),unsafe_allow_html=True)
        st.write(df.to_html(escape=False, index=False), unsafe_allow_html=True)
    # link = '[Notice 1](results/full_results_UMLRM0001.html)'
    # st.markdown(link, unsafe_allow_html=True)"""    
    # HtmlFile = open("results/full_results_UMLRM0001.html", 'r', encoding='utf-8')
    # source_code = HtmlFile.read() 
    # components.html(source_code, height=1200)"""


def make_clickable(label, link):
    # target _blank to open new window
    # extract clickable text to display for your link
    return f'<a target="_blank" href="{link}">{label}</a>'


def st_generate_short_result(entityid, entity, i):
    short_result = []
    short_result.append(f"{str(i)}. {entity.label}")
    version = "version"
    if len(entity.toExpressions)> 1:
        version = "versions"
    ex = "exemplaire"
    if len(entity.toItems) > 1:
        ex = "exemplaires"
    short_result.append(f"    {str(len(entity.toExpressions))} {version}, {str(len(entity.toItems))} {ex}")
    return "\n".join(short_result)


if __name__ == "__main__":
    launch_app()