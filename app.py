import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
import dash
from jupyter_dash import JupyterDash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')
intro = '''
The gender wage gap is a phenonmenon that women, and especially women of color, make signifincatly less money than their male counterparts. The current number is about 82 cents made by a white woman per dollar made by a man. This gap has become especially consequential over the last 50 years as women have become more and more prevalent in the workforce. This difference can be attributed to differences in the jobs women have access to, hours they are offered and able to work, experience women can get in the workforce, and pay discrimination, which is especially prevalent in non unionized industries. Lots of these impacts are based in historical policy and access to resources, like education, networking connections, and industries.

The GSS is a survey focused on social perspectives in America. These include opinions and attitudes on social dynamics and norms, and has been going for 80 years. It allows for researchers and sociologists to make comparisons around societal views and is comprehensive and nationally representative. It is based on personal interviews to get to the root of more complicated social questions like racism and sexism.

https://www.americanprogress.org/article/quick-facts-gender-wage-gap/
'''
p2_table = gss_clean.groupby('sex').agg({'income':'mean','job_prestige':'mean','socioeconomic_index':'mean','education':'mean'}).round(2).reset_index()
p2_table = p2_table.rename(columns={'sex':'Sex','income':'Income','job_prestige':'Job Prestige','socioeconomic_index':'Socioeconomic Status','education':'Years of Education'})
table = ff.create_table(p2_table)
table.show()
barplot_df = gss_clean.groupby(['male_breadwinner', 'sex']).size().to_frame().reset_index().rename({0:'Count'},axis=1)
barplot = px.bar(barplot_df, 
                 x='male_breadwinner', 
                 y='Count', 
                 color='sex', 
                 barmode='group', 
                 labels={'Count': 'Count', 'male_breadwinner': 'Agreement by Gender with the Male Breadwinner Statement'})
barplot
scatter_df = gss_clean[['job_prestige','income','education','socioeconomic_index','sex']]
scatter_df.groupby('sex')
scatter = px.scatter(scatter_df,x='job_prestige',y='income', color='sex',trendline='ols',hover_data=['education','socioeconomic_index'], labels={'count':'Count','income':'Income','job_prestige':'Job Prestige'})
scatter
boxplot1 = px.box(gss_clean,x='sex',y='income', labels={'sex':'','income':'Income'})
boxplot2 = px.box(gss_clean,x='sex',y='job_prestige', labels={'sex':'','job_prestige':'Job Prestige'})
boxplot1.show()
boxplot2.show()
p6_df = gss_clean[['income', 'sex', 'job_prestige']]

p6_df['job_prestige_cat'] = pd.cut(p6_df['job_prestige'], 
                                        bins=[15.0, 26, 37, 
                                              48, 58, 69, 81.0],
                                        labels=['Weakest', 'Weak', 'Slightly Weak', 
                                                'Slightly Strong','Strong', 'Strongest'])
p6_df = p6_df.dropna()
p6_df

facet_box = px.box(p6_df, x="income", y="sex", color_discrete_map = {'male':'blue', 'female':'red'},
             facet_col="job_prestige_cat", facet_col_wrap=2)
facet_box.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_cat=", "")))
facet_box.show()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = JupyterDash(__name__, external_stylesheets=external_stylesheets)
mymarkdowntext = intro

app.layout = html.Div([
    html.H1("Gender Divisions in the GSS Study"),

    html.H2("Tabel of Mean Values by Gender"),

    dcc.Graph(figure = table),
    
    html.H2("Is it much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family?"),

    dcc.Graph(figure = barplot),

    html.H2("Income as a Function of Job Prestige"),

    dcc.Graph(figure = scatter),

    html.H2("Income and Job Prestige Distriubtion by Gender"),
    
    html.Div([
            html.Div([
                html.H3("Income Distribution"),
                dcc.Graph(figure = boxplot1)
            ], style = {'width':'48%','float':'left'}),
            html.Div([
                html.H3("Job Prestige Distribution"),
                dcc.Graph(figure = boxplot2)],
                style = {'width':'48%','float':'right'}),
            ]),
    html.H2("Income Distriubtion for Different Job Prestiges"),

    dcc.Graph(figure = facet_box)
    
])



#step 1 create dropdown, step 2 put callback, which is saying apply these inputs as params to next function, then step 3 output to graph

if __name__=='__main__':
    app.run_server(debug=True)
