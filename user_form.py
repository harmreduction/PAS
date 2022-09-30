
import streamlit as st
import uuid
import geonamescache
from query_db import post_to_db, return_db, analysis_init
from lib.orga_lib import load_orga_lib
from lan.load_specs import load_specs

orga_dict = load_orga_lib()

gc = geonamescache.GeonamesCache()
countries = gc.get_countries()
cities_all=gc.get_cities()


def render_other(dict_out, place_holders,  var_name, guidelines, interface_dict):
    with dict_out[place_holders[0]]:
        if var_name[0] not in ['reasons_dc_visit','knowledge_harmreduction']:
            dict_out[var_name[0]] = st.selectbox(guidelines[var_name[0]]["VARIABLE_NAME"], options=guidelines[var_name[0]]["VOCABULARY"])
        else:
            dict_out[var_name[0]] = st.multiselect(guidelines[var_name[0]]["VARIABLE_NAME"],
                                                 options=guidelines[var_name[0]]["VOCABULARY"])
    if len(var_name) == 1:
        with dict_out[place_holders[1]]:
            if interface_dict["other"] in dict_out[var_name[0]]:
                dict_out[var_name[0]] += [st.text_input(f"{interface_dict['other_option']} {guidelines[var_name[0]]['DESCRIPTION']}")]

    elif len(var_name) == 2:
        with dict_out[place_holders[1]]:
            if dict_out[var_name[0]] == interface_dict["yes_trigger"]:
                dict_out[var_name[1]] = st.multiselect(guidelines[var_name[1]]["VARIABLE_NAME"],
                                                        options=guidelines[var_name[1]]["VOCABULARY"])
                with dict_out[place_holders[2]]:
                    if interface_dict["other"] in dict_out[var_name[1]]:
                        dict_out[var_name[1]] += [
                            st.text_input(f"{interface_dict['other_option']} {guidelines[var_name[1]]['VARIABLE_NAME']}")]


def user_form(username):

    # Load TEDI guidelines
    lang_main = orga_dict[username]["lan"]
    interface_dic = load_specs(lang_main, "interface")['_interface']
    core_guidelines = load_specs(lang_main, "specs")["TEDI"]
    deliberar_guidelines = load_specs(lang_main, "specs")['DELIBERAR']

    required_core_fields = [x for x in core_guidelines if core_guidelines[x]["REQUIREMENT_LEVEL"] == 'required']
    required_deliberar_fields = [x for x in deliberar_guidelines if deliberar_guidelines[x]["REQUIREMENT_LEVEL"] == 'required']

    country_list = [countries[x]['name'] for x in countries]
    country_list.insert(0, country_list.pop(country_list.index(orga_dict[username]['country_first'])))

    # Streamlit widgets to let user create a new post

    h1, h2, h3 = st.columns(3)
    with h1:
        st.header(f" {interface_dic['form_tittle']}")

    with h3:
        head_0 = orga_dict[username]['head']
        st.markdown(head_0, unsafe_allow_html=True)


    with st.form("Sample Form"):

        col1, col2 = st.columns(2)

        with col1:
            # TEDI fields
            head1 = f' [<img src="https://static.wixstatic.com/media/7789af_888c7bc943014bea906377db4d6f2e32~mv2.png/v1/crop/x_136,y_514,w_3267,h_922/fill/w_304,h_85,al_c,q_85,usm_0.66_1.00_0.01,enc_auto/logo%20%23deliberar.png" alt="drawing"/>](https://www.tedinetwork.org/)'
            st.markdown(head1, unsafe_allow_html=True)

            tedi_fields = {"organisation": orga_dict[username]['name'],
                           "date":  str(st.date_input(core_guidelines["date"]["VARIABLE_NAME"])),
                           "placeholder_country": st.empty(),
                           "placeholder_city": st.empty(),
                           "service_type": st.selectbox(core_guidelines["service_type"]["VARIABLE_NAME"],
                                                        options=core_guidelines["service_type"]["VOCABULARY"]),
                           "placeholder_gender": st.empty(),
                           "placeholder_other_gen": st.empty(),
                           "age": st.selectbox(core_guidelines["age"]["VARIABLE_NAME"], options=range(0, 110)),
                           "sold_as": st.selectbox(core_guidelines["sold_as"]["VARIABLE_NAME"],
                                                   options=core_guidelines["sold_as"]["VOCABULARY"]),
                           "sample_form": st.selectbox(core_guidelines["sample_form"]["VARIABLE_NAME"],
                                                       options=core_guidelines["sample_form"]["VOCABULARY"]),
                           "unit_price": st.number_input(core_guidelines["unit_price"]["VARIABLE_NAME"]),
                           "placeholder_unit_substance": st.empty(),
                           "placeholder_other_unit_substance": st.empty(),
                           "colour": st.color_picker(core_guidelines["colour"]["VARIABLE_NAME"], key="12"),
                           "geo_context": st.selectbox(core_guidelines["geo_context"]["VARIABLE_NAME"],
                                                       options=core_guidelines["geo_context"]["VOCABULARY"]),
                           "provider_relation": st.selectbox(core_guidelines["provider_relation"]["VARIABLE_NAME"],
                                                             options=core_guidelines["provider_relation"]["VOCABULARY"]),
                           "alias": st.text_input(core_guidelines["alias"]["VARIABLE_NAME"], key="9"),
                           "used_prior": st.selectbox(core_guidelines["used_prior"]["VARIABLE_NAME"],
                                              options=core_guidelines["used_prior"]["VOCABULARY"]),
                           "logo": st.text_input(core_guidelines["logo"]["VARIABLE_NAME"], key="13")
                           }

        with col2:
            # Deliberar fields
            delib_fields = {
                "placeholder_use_form": st.empty(),
                "placeholder_other_use_form": st.empty(),
                "use_frequency": st.selectbox(deliberar_guidelines["use_frequency"]["VARIABLE_NAME"],
                                              options=deliberar_guidelines["use_frequency"]["VOCABULARY"]),
                "placeholder_effect_unexp": st.empty(),
                "placeholder_list_effect_unexp": st.empty(),
                "placeholder_other_effect_unexp": st.empty(),
                "placeholder_overdose": st.empty(),
                "placeholder_other_overdose": st.empty(),
                "placeholder_overdose_subst": st.empty(),
                "awareness_dc_services": st.selectbox(deliberar_guidelines["awareness_dc_services"]["VARIABLE_NAME"],
                                                      options=deliberar_guidelines["awareness_dc_services"]["VOCABULARY"],
                                                      key="15"),
                "previous_use_dc": st.selectbox(deliberar_guidelines["previous_use_dc"]["VARIABLE_NAME"],
                                                options=deliberar_guidelines["previous_use_dc"]["VOCABULARY"], key="16"),
                "placeholder_reasons_dc_visit": st.empty(),
                "placeholder_other_reasons_dc_visit": st.empty(),
                "placeholder_knowledge_harmred": st.empty(),
                "placeholder_other_knowledge_harmred": st.empty(),
                "use_intention_positiv_result": st.selectbox(deliberar_guidelines["use_intention_positiv_result"]["VARIABLE_NAME"],
                                                             options=deliberar_guidelines["use_intention_positiv_result"]["VOCABULARY"],
                                                             key="17"),
                "use_intention_negativ_result": st.selectbox(deliberar_guidelines["use_intention_negativ_result"]["VARIABLE_NAME"],
                                                             options=deliberar_guidelines["use_intention_negativ_result"]["VOCABULARY"],
                                                             key="18"),
                "service_perception_1": st.selectbox(deliberar_guidelines["service_perception_1"]["VARIABLE_NAME"],
                                                     options=deliberar_guidelines["service_perception_1"]["VOCABULARY"],
                                                     key="19"),
                "service_perception_2": st.selectbox(deliberar_guidelines["service_perception_2"]["VARIABLE_NAME"],
                                                     options=deliberar_guidelines["service_perception_2"]["VOCABULARY"],
                                                     key="20"),
                "service_perception_3": st.selectbox(deliberar_guidelines["service_perception_3"]["VARIABLE_NAME"],
                                                     options=deliberar_guidelines["service_perception_3"]["VOCABULARY"],
                                                     key="21"),

            }

        st.markdown(f"##### {interface_dic['req_field']}")
        submit = st.form_submit_button(f" {interface_dic['submit_form']}")

    # conditional fields

    with tedi_fields["placeholder_country"]:
        input_country = st.selectbox(core_guidelines["country"]["VARIABLE_NAME"], options=country_list, key="4")
        tedi_fields["country"] = [x for x in countries if countries[x]['name'] == input_country][0]

    with tedi_fields["placeholder_city"]:
        country_cities = [""]+[cities_all[x]['name'] for x in cities_all if
                          cities_all[x]['countrycode'] == tedi_fields["country"]]
        tedi_fields["city"] = st.selectbox(core_guidelines["city"]["VARIABLE_NAME"], options=country_cities, key=" 5")

    render_other(tedi_fields, ["placeholder_gender", "placeholder_other_gen"], ["gender"],
                 core_guidelines, interface_dic)

    render_other(tedi_fields, ["placeholder_unit_substance",  "placeholder_other_unit_substance"],
                 ["unit_substance"], core_guidelines, interface_dic)

    place_holders_effect_unx = ["placeholder_effect_unexp", "placeholder_list_effect_unexp",
                                "placeholder_other_effect_unexp"]
    place_holders_od = ["placeholder_effect_unexp", "placeholder_list_effect_unexp",
                                "placeholder_other_effect_unexp"]

    render_other(delib_fields, place_holders_effect_unx, ["effect_unexpected", "effects"],
                 deliberar_guidelines, interface_dic)
    render_other(delib_fields, place_holders_od,  ["overdose", "suspected_od_substance"],
                 deliberar_guidelines, interface_dic)

    render_other(delib_fields, ["placeholder_use_form", "placeholder_other_use_form"],
                 ["use_form"], deliberar_guidelines, interface_dic)
    render_other(delib_fields, ["placeholder_reasons_dc_visit", "placeholder_other_reasons_dc_visit"]
                 ,  ["reasons_dc_visit"], deliberar_guidelines, interface_dic)
    render_other(delib_fields, ["placeholder_knowledge_harmred", "placeholder_other_knowledge_harmred"],
                 ["knowledge_harmreduction"], deliberar_guidelines, interface_dic)

    if submit:

        submit_dict = analysis_init | tedi_fields | delib_fields
        submit_dict = {x: submit_dict[x] for x in submit_dict if not x.startswith("placeholder")}

        if submit_dict["organisation"] and submit_dict['sample_form'] and submit_dict['sold_as']:

            submit_dict["sample_uid"] = str(uuid.uuid4())[:8]
            st.info(f"### {interface_dic['sample_id']}: {submit_dict['sample_uid']}")


            dic_set = {
                submit_dict["sample_uid"]: submit_dict}

            st.text(f"{submit_dict['sample_uid']}, {str(tedi_fields['organisation'])}, {submit_dict}")
            post_to_db(dic_set, submit_dict["sample_uid"])

        else:

            missing_fields = ['organisation', 'sample_form', 'sold_as']
            st.warning(f"{interface_dic['warning_req_fields']} \n {missing_fields}")

    if st.button(interface_dic['show_db']):

        st.dataframe(return_db()[1])