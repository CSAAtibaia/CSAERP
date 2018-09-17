from cep.widgets import CEPInput


my_cep_field = ChangeToMyCEPFieldModelName(label=u"CEP",
                        help_text="Format: XXXXX-XXX",
                        widget=CEPInput(address={
                                                 'street': 'id_street_field',
                                                 'district': 'id_district_field',
                                                 'city': 'id_city_field',
                                                 'state': 'id_state_field'
                                                 }))