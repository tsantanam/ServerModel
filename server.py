from flask import Flask, render_template, jsonify, request, Response, url_for, redirect
import pandas as pd
import random
import os
import folium
from datetime import datetime
from jinja2 import Template
app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['GET','POST'])
def index():
    if os.path.exists("/home/atldotbus/WebModel/input.csv"):
          os.remove("/home/atldotbus/WebModel/input.csv")
    if os.path.exists("/home/atldotbus/WebModel/templates/index2.html"):
        os.remove("/home/atldotbus/WebModel/templates/index2.html")
    if os.path.exists("/home/atldotbus/WebModel/templates/map.html"):
        os.remove("/home/atldotbus/WebModel/templates/map.html")
    if os.path.exists("/home/atldotbus/WebModel/templates/map2.html"):
        os.remove("/home/atldotbus/WebModel/templates/map2.html")
    else:
        print("The file does not exist")
    return render_template('index.html')


@app.route('/funding-allocation/', methods=['GET','POST'])
def funding_allocation():

  if 'submit_button3' in request.form:
      if request.method == 'POST':
          if os.path.exists("/home/atldotbus/WebModel/input.csv"):
              os.remove("/home/atldotbus/WebModel/input.csv")
          if os.path.exists("/home/atldotbus/WebModel/templates/index2.html"):
              os.remove("/home/atldotbus/WebModel/templates/index2.html")
          if os.path.exists("/home/atldotbus/WebModel/templates/map.html"):
              os.remove("/home/atldotbus/WebModel/templates/map.html")
          if os.path.exists("/home/atldotbus/WebModel/templates/map2.html"):
              os.remove("/home/atldotbus/WebModel/templates/map2.html")
          try:
              f = request.files['file']
              f.save('/home/atldotbus/WebModel/'+f.filename)
          except:
              return render_template('index.html', result=None)
          if os.path.exists("/home/atldotbus/WebModel/input.csv") and request.form['budget_input']!='':
              if float(request.form['budget_input']) > 0:
                  return render_template('index.html', result=(float(request.form['budget_input'])))
              else:
                  return render_template('index.html', result=0)
          else:
              return render_template('index.html', result=None)


  if 'submit_button1' in request.form or 'submit_button2' in request.form:
      if request.method == 'POST':
          budget_input = float(request.form['budget_input'])
      print(budget_input, "+++++++++++++++++++++++++++++")
      ###Input stop file and budget
      if os.path.exists("/home/atldotbus/WebModel/input.csv"):
          df = pd.read_csv("/home/atldotbus/WebModel/input.csv")
      else:
          print("No file found")
      if budget_input>0:
          budget1 = budget_input
      else:
          budget1 = 0
      print(budget1, "===========================================")
      # Data pre-processing

      #Checking for errors in input file
       #column name
      try:
          df['StopAbbr'].tolist()
      except:
          return render_template('index.html', errortype='StopAbbr column name')

      try:
         df['ADA_ACCESS'].tolist()
      except:
          return render_template('index.html', errortype='ADA_ACCESS column name')

      try:
          df['BASE'].tolist()
      except:
          return render_template('index.html', errortype='BASE column name')

      try:
          df['Ons'].tolist()
      except:
          return render_template('index.html', errortype='Ons column name')

      try:
          df['Stop_Type'].tolist()
      except:
          return render_template('index.html', errortype='Stop_Type column name')

      try:
          df['Poss'].tolist()
      except:
          return render_template('index.html', errortype='Poss column name')

      try:
          df['ROW'].tolist()
      except:
          return render_template('index.html', errortype='ROW column name')

      try:
          df['Latitude'].tolist()
      except:
          return render_template('index.html', errortype='Latitude column name')

      try:
          df['Longitude'].tolist()
      except:
          return render_template('index.html', errortype='Longitude column name')

      #column name
      StopAbbr = df['StopAbbr'].tolist()
      ADA_ACCESS = df['ADA_ACCESS'].tolist()
      BASE = df['BASE'].tolist()
      Ons = df['Ons'].tolist()
      Stop_Type = df['Stop_Type'].tolist()
      Poss = df['Poss'].tolist()
      ROW = df['ROW'].tolist()
      Lat = df['Latitude'].tolist()
      Long = df['Longitude'].tolist()

      #data type
      remove_row = []
      for i in range(0,len(StopAbbr)):
          if (type(StopAbbr[i]) != int) and (type(StopAbbr[i] != str)):
              remove_row.append(i)
              #return render_template('index.html', errortype='StopAbbr datatype')
      #print(remove_row)
      for i in range(0,len(ADA_ACCESS)):
          if (ADA_ACCESS[i] != "Y") and (ADA_ACCESS[i] != "N"):
              remove_row.append(i)
              #return render_template('index.html', errortype='ADA_ACCESS datatype')
      #print(remove_row)
      for i in range(0,len(BASE)):
          if (BASE[i] != "DIRT") and (BASE[i] != "CONC"):
              remove_row.append(i)
              #return render_template('index.html', errortype='BASE datatype')
      #print(remove_row)
      for i in range(0,len(Ons)):
          try:
              float(Ons[i])
          except:
              remove_row.append(i)
              #return render_template('index.html', errortype='Ons column name')
      #print(remove_row)
      for i in range(0,len(Stop_Type)):
          if (Stop_Type[i] != 'Sign') and (Stop_Type[i] != 'Simme Seat') and (Stop_Type[i] != 'MARTA Bench') and (Stop_Type[i] != 'MARTA Shelter') and (Stop_Type[i] != 'Other Shelter') and (Stop_Type[i] != 'Other Bench') and (Stop_Type[i] != 'Station'):
              remove_row.append(i)
              #return render_template('index.html', errortype='Stop_Type column name')
      for i in range(0,len(Poss)):
          try:
              if (int(Poss[i]) != 0) and (int(Poss[i]) != 1):
                  remove_row.append(i)
          except:
              remove_row.append(i)
      #print(remove_row)
      for i in range(0,len(ROW)):
          try:
              float(ROW[i])
          except:
              remove_row.append(i)

      for i in range(0,len(Lat)):
          try:
              float(Lat[i])
          except:
              remove_row.append(i)

      for i in range(0,len(Long)):
          try:
              float(Long[i])
          except:
              remove_row.append(i)

      remove_row = list(dict.fromkeys(remove_row))
      print(remove_row)

      remove_row_message = []
      for i in remove_row:
          remove_row_message.append(i + 2)


      # MARTA Stop Data
      Stops1 = df['StopAbbr'].drop(remove_row,axis=0).tolist()
      ridership1 = df['Ons'].drop(remove_row,axis=0).tolist()
      numStops1 = len(df['StopAbbr'].drop(remove_row,axis=0).tolist())
      n1 = range(numStops1)

      # Unsolvable Observations
      poss1 = df['Poss'].drop(remove_row,axis=0).tolist()
      poss1 = [int(n) for n in poss1]

      # # Simulated ROW  ##(simulated to real when data is available)
      # row = [0] * numStops1
      # for n in range(numStops1):
      #     x = random.random()
      #     if x > .5:
      #         row[n] = int(random.randint(20000, 40000))
      row=df['ROW'].drop(remove_row,axis=0).tolist()
      row=[int(n) for n in row]

      Lat = df['Latitude'].drop(remove_row, axis=0).tolist()
      Lat = [float(n) for n in Lat]

      Long = df['Longitude'].drop(remove_row, axis=0).tolist()
      Long = [float(n) for n in Long]


      # Existing amenity score calculation
      amenityscore = []
      for i in n1:
          if df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'DIRT' and df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Sign' and poss1[i]==0:
              amenityscore.append(0)
          elif (df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC' and df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Sign') and poss1[i]==0:
              amenityscore.append(0)
          elif df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'DIRT' and df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Sign':
              amenityscore.append(1)
          elif (df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC' and df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Sign'):
              amenityscore.append(2)
          elif df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'MARTA Bench' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Other Bench' or \
                  df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Simme Seat':
              amenityscore.append(3)
          elif (df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'MARTA Shelter' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Other Shelter') and \
                  df['ADA_ACCESS'].drop(remove_row,axis=0).tolist()[i] != 'Y':
              amenityscore.append(4)
          elif (df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'MARTA Shelter' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Other Shelter') and \
                  df['ADA_ACCESS'].drop(remove_row,axis=0).tolist()[i] == 'Y' or df['Stop_Type'].drop(remove_row,axis=0).tolist()[i] == 'Station':
              amenityscore.append(5)
      # Amenity Costs
      simmeseat_cost = 500
      simmeseat_install_np_tc = 5500
      simmeseat_install_sw = 700

      bench_cost = 5000  # survey and design + bench kit
      bench_install_sw = 1000  # installation cost on existing sidewalk
      bench_install_np = 3000  # installation cost on new pad

      shelter_cost = 13000  # survey and design + shelter kit
      shelter_install_sw = 6000  # installation cost on existing sidewalk
      shelter_install_np = 10000  # installation cost on new pad

      # Calculating cost of amenity needs for each stop
      need = [[0, 0, 0] for i in n1]
      for i in n1:
          if amenityscore[i] < 3:
              if df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC':
                  ss_cost = simmeseat_cost + simmeseat_install_sw
                  b_cost = bench_cost + bench_install_sw
              else:
                  ss_cost = simmeseat_cost + simmeseat_install_np_tc
                  b_cost = bench_cost + bench_install_np
              need[i][0] = ss_cost
              need[i][1] = b_cost
          if amenityscore[i] < 4:
              if df['BASE'].drop(remove_row,axis=0).tolist()[i] == 'CONC':
                  sh_cost = shelter_cost + shelter_install_sw
              else:
                  sh_cost = shelter_cost + shelter_install_np
              need[i][2] = sh_cost

      # Calculation of equity score
      #equityscore1 = []
      #for i in range(0, len(Stops1)):
      #    equityscore1.append(incomeweight * (1 - avgincome1[i] / max(avgincome1)) + nocarweight * (
      #            nocar1[i] / max(nocar1)) + populationweight * ((population1[i]) / max(population1)))
      # Greedy heuristic
      funding = [0] * numStops1
      fincost = [0] * numStops1
      indexList=[i[0] for i in sorted(enumerate(ridership1), key=lambda k: k[1], reverse=True)]
      # indexList = [i[0] for i in sorted(enumerate([a * b for a, b in zip(ridership1, equityscore1)]),
      #                                   key=lambda k: k[1], reverse=True)]

      forvars = [
          # [need vector, unsolvable included, lower acceptable score, upper acceptable score, ROW not included, need position in list]
          [need, False, 0, 4, True, 2],
          [need, False, 0, 4, False, 2],
          [need, False, 0, 3, True, 1],
          [need, False, 0, 3, False, 1],
          [need, True, 0, 3, True, 0],
          [need, True, 0, 3, False, 0]
      ]

      for f in forvars:
          for x in n1:
              s=indexList[x]
              if f[0][s][f[5]] > 0 and budget1 >= f[0][s][f[5]] + row[s] and funding[s] == 0 and (
                      f[1] or amenityscore[s] > f[2]) and amenityscore[s] < f[3] and (row[s] != 0 or f[4]):
                  funding[s] = f[0][s][f[5]] + row[s]
                  fincost[s] = f[0][s][f[5]]
                  budget1 -= f[0][s][f[5]] + row[s]


      for i in n1:
          if poss1[i]==0 and amenityscore[i]>=3:
              funding[i]=0
              fincost[i]=0


      # Amenity Recommendation
      amenitytype = []
      for s in n1:
          if fincost[s] == 19000 or fincost[s] == 23000:
              amenitytype.append("Shelter")
          if fincost[s] == 8000 or (fincost[s] == 6000 and df['BASE'].tolist()[s] == 'CONC'):
              amenitytype.append("Bench")
          if fincost[s] == 1200 or (fincost[s] == 6000 and df['BASE'].tolist()[s] != 'CONC'):
              amenitytype.append("Simme Seat")
          if fincost[s] == 0:
              amenitytype.append('None')

      # New amenity score calculation
      newscore = []
      for i in n1:
          if amenitytype[i] == 'Shelter' and df['ADA_ACCESS'].tolist()[i] != 'Y':
              newscore.append(4)
          if amenitytype[i] == 'Shelter' and df['ADA_ACCESS'].tolist()[i] == 'Y':
              newscore.append(5)
          if amenitytype[i] == 'Simme Seat' or amenitytype[i] == 'Bench':
              newscore.append(3)
          if amenitytype[i] == 'None':
              newscore.append(amenityscore[i])

      # Output exporting to CSV

      df2 = pd.DataFrame()
      df2['Stop_ID'] = Stops1
      df2['Funding'] = funding
      df2['Amenity_Type'] = amenitytype
      df2['Current_Score'] = amenityscore
      df2['New_Score'] = newscore
      df2['Daily_Ridership'] = [int(float(n)) for n in ridership1]

      ###### Summary ######
      #total ridership impacted, #total funding, #average new amenity score
      totalRiders = sum([int(float(n[1])) for n in enumerate(ridership1) if int(funding[n[0]]) > 0])
      totalFunding = sum(funding)
      avgCAS = round(sum(amenityscore)/len(amenityscore),3)
      avgNAS = round(sum(newscore)/len(newscore),3)

      df3 = pd.DataFrame()
      df3['Total Riders Impacted'] = [totalRiders]
      df3['Total Funding Used'] = [totalFunding]
      df3['Average Current Amenity Score'] = [avgCAS]
      df3['Average New Amenity Score'] = [avgNAS]
      df3['Stops Funded'] = [sum(i > 0 for i in funding)]

      df4 = pd.DataFrame()
      df4['Stop_ID'] = Stops1
      df4['Amenity_Type'] = amenitytype
      df4['Latitude'] = Lat
      df4['Longitude'] = Long
      df4['Current Amenity Score'] = amenityscore
      df4['New Amenity Score'] = newscore

      map = folium.Map(location=[df4.Latitude.mean(), df4.Longitude.mean()],
                       zoom_start=12, control_scale=True)
      maprows = [[x, y, z, a, b, c] for x, y, z, a, b, c in zip(df4['Latitude'], df4['Longitude'], df4['Stop_ID'], df4['Amenity_Type'], df4['Current Amenity Score'], df4['New Amenity Score'])]
      map1 = folium.FeatureGroup(name='None')
      map2 = folium.FeatureGroup(name='Simme Seat')
      map3 = folium.FeatureGroup(name='Bench')
      map4 = folium.FeatureGroup(name='Shelter')

      for n in maprows:
          html='<div style="text-align:center;"><b>ID</b>: '+str(n[2])+'<br>  <b>Current</b>: '+str(n[4])+' ➔  <b>New</b>: '+str(n[5])+'<br> <b>Amenity</b>: '+str(n[3])+'<div>'
          iframe = folium.IFrame(html,
                                 width=200,
                                 height=75)

          popup = folium.Popup(iframe,
                               max_width=200)
          if n[3] == 'None':
              folium.Marker([n[0], n[1]], icon=folium.Icon(color='black'), popup=popup).add_to(map1)
          if n[3] == 'Simme Seat':
              folium.Marker([n[0], n[1]], icon=folium.Icon(color='blue'),popup=popup).add_to(map2)
          if n[3] == 'Bench':
              folium.Marker([n[0], n[1]], icon=folium.Icon(color='red'),popup=popup).add_to(map3)
          if n[3] == 'Shelter':
              folium.Marker([n[0], n[1]], icon=folium.Icon(color='green'),popup=popup).add_to(map4)

      map.add_child(map1)
      map.add_child(map2)
      map.add_child(map3)
      map.add_child(map4)

      # turn on layer control
      map.add_child(folium.map.LayerControl())
      map.save('/home/atldotbus/WebModel/templates/map.html')

      priorityList=[0]*numStops1
      count=0
      for n in n1:
          if funding[indexList[n]]!=0:
              count+=1
              priorityList[indexList[n]]=count
      for n in n1:
          if funding[indexList[n]]==0:
              count+=1
              priorityList[indexList[n]]=count
      df2['Priority'] = priorityList

      if 'submit_button2' in request.form:
          dt = datetime.now().strftime("%m_%d_%Y")
          return  Response(
              df2.sort_values('Priority').to_csv(index=False),
              mimetype="text/csv",
              headers={"Content-disposition": "attachment; filename=HeuristicOutput_" + dt + ".csv"})

# Updated with SummaryStat
      if 'submit_button1' in request.form:
          result = df2.sort_values('Priority').to_html(index=False)
          result1 = '<span class="text">Daily Riders Impacted: %s</span>' % df3['Total Riders Impacted'][0]
          result2 = '<span class="text">Funding Allocated: %s</span>' % df3['Total Funding Used'][0]
          result3 = '<span class="text">Avg Current Score: %s</span>' % df3['Average Current Amenity Score'][0]
          result4 = '<span class="text">Avg New Score: %s</span>' % df3['Average New Amenity Score'][0]
          result5 = '<span class="text">Stops Funded: %s</span>' % df3['Stops Funded'][0]

          with open('/home/atldotbus/WebModel/base/index2.html') as f:
              t = Template(f.read())

            # Create a dict with template keys and their values
          if remove_row_message != []:
              vals = {'replace_me': result, 'replace_me1': result1, 'replace_me2': result2, 'replace_me3': result3, 'replace_me4': result4, 'replace_me5': result5, 'row_list':remove_row_message}
          else:
              vals = {'replace_me': result, 'replace_me1': result1, 'replace_me2': result2, 'replace_me3': result3, 'replace_me4': result4, 'replace_me5': result5}

          f = open('/home/atldotbus/WebModel/templates/index2.html', 'w')
          f.write(t.render(vals))
          f.close()

          return render_template('index2.html',result=df2.to_dict())




  if 'reset1' in request.form:
      if os.path.exists("/home/atldotbus/WebModel/input.csv"):
          os.remove("/home/atldotbus/WebModel/input.csv")
      if os.path.exists("/home/atldotbus/WebModel/templates/index2.html"):
          os.remove("/home/atldotbus/WebModel/templates/index2.html")
      if os.path.exists("/home/atldotbus/WebModel/templates/map.html"):
          os.remove("/home/atldotbus/WebModel/templates/map.html")
      if os.path.exists("/home/atldotbus/WebModel/templates/map2.html"):
          os.remove("/home/atldotbus/WebModel/templates/map2.html")
      else:
          print("The file does not exist")
      #webbrowser.open('https://www.atldotbus.pythonanywhere.com')
      return render_template('index.html', result=None)
@app.route('/map')
def map():
    return render_template('map.html')
@app.route('/map2', methods=['GET','POST'])
def map2():
    if request.method == 'POST':
        if os.path.exists("/home/atldotbus/WebModel/templates/map2.html"):
            os.remove("/home/atldotbus/WebModel/templates/map2.html")
        index_text = request.data
        print("index text: ", (index_text.decode("utf-8").split(',')))
        maprows = (index_text.decode("utf-8").split(','))
        df = pd.read_csv("/home/atldotbus/WebModel/input.csv")
        lat = df['Latitude'].tolist()[int(maprows[6])]
        long = df['Longitude'].tolist()[int(maprows[6])]
        map2 = folium.Map(location=[lat,long],
                     zoom_start=12, control_scale=True)
        html = '<div style="text-align:center;"><b>ID</b>: ' + str(maprows[0]) + '<br>  <b>Current</b>: ' + str(
            maprows[3]) + ' ➔  <b>New</b>: ' + str(maprows[4]) + '<br> <b>Amenity</b>: ' + str(maprows[2]) + '<div>'
        iframe = folium.IFrame(html,
                               width=200,
                               height=75)

        popup = folium.Popup(iframe,
                             max_width=200)
        if maprows[2] == 'None':
            folium.Marker([lat,long], icon=folium.Icon(color='black'), popup=popup).add_to(map2)
        if maprows[2] == 'Simme Seat':
            folium.Marker([lat,long], icon=folium.Icon(color='blue'), popup=popup).add_to(map2)
        if maprows[2] == 'Bench':
            folium.Marker([lat,long], icon=folium.Icon(color='red'), popup=popup).add_to(map2)
        if maprows[2] == 'Shelter':
            folium.Marker([lat,long], icon=folium.Icon(color='green'), popup=popup).add_to(map2)
        map2.save('/home/atldotbus/WebModel/templates/map2.html')
    return render_template('map2.html')
@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r
if __name__ == '__main__':
  app.run(debug=True)