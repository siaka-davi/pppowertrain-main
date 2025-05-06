from django.shortcuts import render
import pandas as pd
import io
from django.http import HttpResponse
from .form import SearchForm
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle




def index(request):
    # Charger votre DataFrame
    df = pd.DataFrame()
    df1 = pd.read_excel('DONNEES_POWERTRAIN_FRANCE.xlsx')
    df2 = pd.read_excel('EV_DATA_BASE_AC_042025.xlsx')
    df = pd.concat([df1,df2])
    #df['Disponibilité'] = df[df['Disponibilité_x']!=' ']["Dispon"] + df[df['Disponibilité_y']!=' ']
    france = ['Modèle','Version','Prix','Disponibilité','Autonomie_WLTP_km','Motorisation','Catégorie','Transmission',
              'Nombre_de_sièges','Accél_0_100 km/h_s','Vitesse_max_km_par_h','Couple_Nm','Type','Consommation_WLTP_kWh_par_100km',
              'Puissance_max_AC_kW','Puissance_max_DC_kW','Puissance_fiscale_CV','Longueur_mm','Largeur_mm','Hauteur_mm','Empattement_mm',
              'Volume du coffre_L','Garde au sol_mm','Poids à vide_kg','Poids_total_autorisé_en_charge_kg','Connecteur_AC','Connecteur_DC_CCS',
              'Coefficient_de_traînée_(Cx)','Rayon_de_braquage_m','Pneumatiques','Emission CO2_g_par_km','Boite de vitesse',
              'Puissance_cumulée_kW','Puissance_thermique_kW','Moteur thermique','Couple thermique_Nm','Puissance électrique_kW',
              'Couple électrique_Nm','Autonomie_Été_Mixte_km','Autonomie_Été_Autoroute_km',
              'Autonomie_Été_Ville_km','Autonomie_Hiver_Mixte_km','Autonomie_Hiver_Autoroute_km','Autonomie_Hiver_Ville_km',
              'Consommation_Été_Mixte_kWh_par_100km','Consommation_Été_Autoroute_kWh_par_100km','Consommation_Été_Ville_kWh_par_100km',
              'Consommation_Hiver_Mixte_kWh_par_100km','Consommation_Hiver_Autoroute_kWh_par_100km','Consommation_Hiver_Ville_kWh_par_100km',
              'Puissance_ch','Puissance_kw','capacité_brut_kwh','capacité_utilisable_kwh']
    autres = ['Pays','Modèle','Prix','Disponibilté','Autonomie_WLTP_km','Conso_WLTP_Wh_100km','Segment','acel 0-100 km/h',
              'Transmission','Nominal_Capacity_kWh','Useable_Capacity_kWh','Charge_Port','Port_Location','Charge_Power_AC_kWh',
              'Power_kW','Power_PS','Motorisation']
    
    Outputice=['Pays', 'Marques', 'Model + Trim + PWT (auto)', 'Modele', 'Trim',
       'PowerTrain','MRSP','ENERGIE_pour_Conso_Green_Image_et_NVH',
       'CARBURANT_pour_conversion_L_km', 'Puissance_ch','Torque(Nm)','Accel_0_a_100km',
        'Turbo(0/1)', 'CO2_g_km','CONSO_L_km', 'GearBox_type', 'nbre_de_rapports', 'type4x4',
       'bonus_malus']

    Outputev=['Pays', 'Marques', 'Model + Trim + PWT (auto)', 'Modele', 'Trim',
       'PowerTrain','MRSP', 'Puissance_ch','Autonomie_km', 'Elec_Conso_kwh_100_km',
        'SOC_int(%)','SOC_fin(%)','durée_de_charge','P_DC_charge_kw','Chargeur_AC',
         'type4x4', 'Precond','PAC', 'MODM_kg','bonus_malus']
    
    #Input1 = ['Pays', 'segment', 'ENERGIE_pour_Conso_Green_Image_et_NVH', 'ICE_XHEV_EV']

    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query_p = form.cleaned_data['query_p']
            query_s = form.cleaned_data['query_s']
            query_e = form.cleaned_data['query_e']
            query_i = form.cleaned_data['query_i']
            query_j = form.cleaned_data['query_j']

            # Effectuer la recherche dans le DataFrame
            if query_p:
                 df = df[df['Pays']==query_p]
                #if query_p=='France':
                    #df = df[df['Pays']==query_p][france]
                #else:
                    #df = df[df['Pays']==query_p][autres]
            if query_s:
                df = df[df['Segment'] == query_s]
            if query_e:
                df = df[df['Disponibilité'] == query_e]
            if query_i:
                df = df[df['Motorisation'] == query_i]
            if query_j:
                df = df[df['Transmission']==query_j]
            
            request.session['filtered_df'] = df.to_json()
    else:
        form = SearchForm()
    
    df_head = df.head(10)

    return render(request, 'counter/index1.html', {'form': form, 'df': df_head})


def download_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Powertrain.csv"'
    df = pd.read_json(request.session.get('filtered_df'))
    df.to_csv(path_or_buf=response, index=False)
    return response

def download_excel(request):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="Powertrain.xlsx"'
    df = pd.read_json(request.session.get('filtered_df'))
    df.to_excel(response, index=False)
    return response

def download_pdf(request):
    # Assurez-vous que le DataFrame filtré est disponible dans la session
    df_json = request.session.get('filtered_df')
    if not df_json:
        return HttpResponse("No data available for PDF download.")
    
    df = pd.read_json(df_json)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Powertrain.pdf"'

    # Create a PDF document
    pdf = SimpleDocTemplate(response, pagesize=letter)
    data = [df.columns.tolist()] + df.values.tolist()
    t = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    t.setStyle(style)
    elems = []
    elems.append(t)
    pdf.build(elems)
    return response