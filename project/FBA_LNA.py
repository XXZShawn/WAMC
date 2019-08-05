def run(model_input,illumination,h,h2o,pi,nh4,no3,so4,o2,ac):
    try:
        import cobra
        DW = 3e-11 # average dry weight of log phase chlamy cell = 48 pg (Mitchell 1992)
        CPerStarch300 = 1800 # derived from starch300 chemical formula
        ChlPerCell = (13.9+4)/(1e7) # 13.9 +- 4 micrograms Chl/10^7 cells (Gfeller 1984)
        starchDegAnLight = (4.95+1.35)*(1/1000)*(1/CPerStarch300)*(ChlPerCell/1000)*(1/DW) # approx. SS rate of anaerobic starch degradation in light = 4.95 +- 1.35 micromol C/mg Chl/hr (Gfeller 1984)
        starchDegAerLight = (2/3)*(4.95+1.35)*(1/1000)*(1/CPerStarch300)*(ChlPerCell/1000)*(1/DW) # approx. SS rate of aerobic starch degradation in light = 2/3 of anaerobic rate (Gfeller 1984)
        starchDegAnDark = (13.1+3.5)*(1/1000)*(1/CPerStarch300)*(ChlPerCell/1000)*(1/DW) # approx. SS rate of anaerobic starch degradation in dark = 13.1 +- 3.5 micromol C/mg Chl/hr (Gfeller 1984)
        starchDegAerDark = (2/3)*starchDegAnDark # approx. SS rate of aerobic starch degradation in dark = 2/3 of anaerobic rate (Gfeller 1984) = 2/3 of anaerobic rate (Gfeller 1984)

        model = cobra.io.read_sbml_model(model_input)
        
        model.reactions.get_by_id("Biomass_Chlamy_auto").objective_coefficient = 1
        model.reactions.get_by_id("Biomass_Chlamy_mixo").objective_coefficient = 0
        model.reactions.get_by_id("Biomass_Chlamy_hetero").objective_coefficient = 0
        if illumination==1:
            pass
        elif illumination==2:
            model.reactions.get_by_id("Biomass_Chlamy_auto").objective_coefficient = 0
            model.reactions.get_by_id("Biomass_Chlamy_mixo").objective_coefficient = 1
        else:
            model.reactions.get_by_id("Biomass_Chlamy_auto").objective_coefficient = 0
            model.reactions.get_by_id("Biomass_Chlamy_hetero").objective_coefficient = 1

        model.reactions.get_by_id("PRISM_solar_litho").upper_bound = 0
        model.reactions.get_by_id("PRISM_solar_litho").lower_bound = 0
        model.reactions.get_by_id("PRISM_solar_exo").upper_bound = 0
        model.reactions.get_by_id("PRISM_solar_exo").lower_bound = 0
        model.reactions.get_by_id("PRISM_incandescent_60W").upper_bound = 0
        model.reactions.get_by_id("PRISM_incandescent_60W").lower_bound = 0
        model.reactions.get_by_id("PRISM_fluorescent_warm_18W").upper_bound = 0
        model.reactions.get_by_id("PRISM_fluorescent_warm_18W").lower_bound = 0
        model.reactions.get_by_id("PRISM_fluorescent_cool_215W").upper_bound = 0
        model.reactions.get_by_id("PRISM_fluorescent_cool_215W").lower_bound = 0
        model.reactions.get_by_id("PRISM_metal_halide").upper_bound = 0
        model.reactions.get_by_id("PRISM_metal_halide").lower_bound = 0
        model.reactions.get_by_id("PRISM_high_pressure_sodium").upper_bound = 0
        model.reactions.get_by_id("PRISM_high_pressure_sodium").lower_bound = 0
        model.reactions.get_by_id("PRISM_growth_room").upper_bound = 0
        model.reactions.get_by_id("PRISM_growth_room").lower_bound = 0
        #model.reactions.get_by_id("PRISM_white_LED").upper_bound = 0
        #model.reactions.get_by_id("PRISM_white_LED").lower_bound = 0
        model.reactions.get_by_id("PRISM_design_growth").upper_bound = 10
        model.reactions.get_by_id("PRISM_design_growth").lower_bound = 10

        model.reactions.get_by_id("EX_h_LPAREN_e_RPAREN_").lower_bound = h
        model.reactions.get_by_id("EX_h2o_LPAREN_e_RPAREN_").lower_bound = h2o
        model.reactions.get_by_id("EX_pi_LPAREN_e_RPAREN_").lower_bound = pi
        model.reactions.get_by_id("EX_nh4_LPAREN_e_RPAREN_").lower_bound = nh4
        model.reactions.get_by_id("EX_no3_LPAREN_e_RPAREN_").lower_bound = no3
        model.reactions.get_by_id("EX_so4_LPAREN_e_RPAREN_").lower_bound = so4
        model.reactions.get_by_id("EX_o2_LPAREN_e_RPAREN_").lower_bound = o2

        model.reactions.get_by_id("EX_ac_LPAREN_e_RPAREN_").lower_bound = ac

        model.reactions.get_by_id("EX_ac_LPAREN_e_RPAREN_").upper_bound = 0
        model.reactions.get_by_id("EX_starch_LPAREN_h_RPAREN_").lower_bound = 0
        model.reactions.get_by_id("EX_starch_LPAREN_h_RPAREN_").upper_bound = 0
        model.reactions.get_by_id("STARCH300DEGRA").upper_bound = starchDegAerLight/2
        model.reactions.get_by_id("STARCH300DEGR2A").upper_bound = 0
        model.reactions.get_by_id("STARCH300DEGRB").upper_bound = starchDegAerLight/2
        model.reactions.get_by_id("STARCH300DEGR2B").upper_bound = 0

        model.reactions.get_by_id("PCHLDR").lower_bound = 0
        model.reactions.get_by_id("PCHLDR").upper_bound = 0
        model.reactions.get_by_id("PFKh").lower_bound = 0
        model.reactions.get_by_id("PFKh").upper_bound = 0
        model.reactions.get_by_id("G6PADHh").lower_bound = 0
        model.reactions.get_by_id("G6PADHh").upper_bound = 0
        model.reactions.get_by_id("G6PBDHh").lower_bound = 0
        model.reactions.get_by_id("G6PBDHh").upper_bound = 0
        model.reactions.get_by_id("FBAh").lower_bound = 0
        model.reactions.get_by_id("FBAh").upper_bound = 0
        model.reactions.get_by_id("H2Oth").upper_bound = 0
        #model.reactions.get_by_id("Biomass_Chlamy_mixo").lower_bound = 0
        #model.reactions.get_by_id("Biomass_Chlamy_mixo").upper_bound = 0
        #model.reactions.get_by_id("Biomass_Chlamy_hetero").lower_bound = 0
        #model.reactions.get_by_id("Biomass_Chlamy_hetero").upper_bound = 0

        LNA_sol = cobra.flux_analysis.parsimonious.optimize_minimal_flux(model)
        pFBA_status=LNA_sol.status
        obj_value=LNA_sol.objective_value
        fluxes=LNA_sol.fluxes
        return pFBA_status,obj_value,fluxes
    except:
        return "ERROR: PLEASE CHANGE THE XML FILE OR CHANGE THE VARIABLES"



    
    



