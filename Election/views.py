from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseForbidden, HttpResponseBadRequest,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext
from django.shortcuts import render_to_response
from .models import Login_data
from itertools import izip
import datetime,time
from django.utils.encoding import smart_str
import json

def render_page(request):
    return render_to_response('Login_page.html', context_instance=RequestContext(request))

@csrf_exempt
# @require_POST
# @login_required
#
#
# 
def portal_render(request):
  username = request.POST.get('mail', '')
  passwd = request.POST.get('Password', '')
  desig = request.POST.get('id','')
  print username
  if username and passwd:
      request.session['username'] = username
      request.session['password'] = passwd
      request.session['desig']   =  desig
  try:
      username = request.session['username']
      passwd = request.session['password']
      desig = request.session['desig']
  except:
      pass
  print username
  content = {};
  query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
  print query
  from django.db import connection
  with connection.cursor() as cursor:
    cursor.execute(query)
    all_data = cursor.fetchall()
    print all_data
    if not all_data:
        return render_to_response('Login_page.html',context_instance=RequestContext(request))
    col_name_list = [desc[0] for desc in cursor.description]
    user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
    print user_data
  query = 'select * from Election_citizens where user_name="'+str(user_data[0]['user_name'])+'"'
  with connection.cursor() as cursor:
      cursor.execute(query)
      content_data = cursor.fetchall()
      content_col_name_list = [desc[0] for desc in cursor.description]
  cont_data=map(lambda z:dict(izip(content_col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), content_data))
  con_data = cont_data[0]
  year = datetime.date.today().year
  query = 'select * from Election_election_duration where election_year="'+str(year)+'"'
  with connection.cursor() as cursor:
      cursor.execute(query)
      election_data = cursor.fetchall();
      print election_data;


  if user_data[0]['designation']==desig or user_data[0]['designation']=="common":
      content['name']=con_data['First_name']+con_data['Last_name']
      content['addr']=con_data['Address']
      content['email']=con_data['email']
      content['contact']=con_data['contact']
      if (time.strptime(str(election_data[0][2]),"%Y-%m-%d") <= time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d")) and (time.strptime(str(election_data[0][1]),"%Y-%m-%d") > time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d")):
        content['delete']="yes"
      else:
        content['delete']="no"
      if desig=="voter":
          content['desig']="voter"
          query = 'select * from Election_vote_casted where user_name = "'+str(user_data[0]['user_name'])+'" and year(casted_year)="'+str(year)+'"'
          with connection.cursor() as cursor:
            cursor.execute(query)
            casted_data = cursor.fetchall();
          if not casted_data:
            content['able_to_vote'] ="yes"
          else:
            content['able_to_vote'] ="no"
          if time.strptime(str(election_data[0][1]),"%Y-%m-%d") == time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d"):
            content['polling']="yes"
          else:
            content['polling']="no"
          if time.strptime(str(election_data[0][1]),"%Y-%m-%d") < time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d"):
            content['result']="yes"
          else:
            content['result']="no"

      elif desig=="admin":
          content['desig']="admin"
          if time.strptime(str(election_data[0][2]),"%Y-%m-%d") == time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d"):
            content['add']="yes"
          else:
            content['add']="no"
          if (time.strptime(str(election_data[0][2]),"%Y-%m-%d") <= time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d")) and (time.strptime(str(election_data[0][1]),"%Y-%m-%d") > time.strptime(str(datetime.date.today().strftime("%Y-%m-%d")),"%Y-%m-%d")):
            content['delete']="yes"
          else:
            content['delete']="no"
  else:
      return render_to_response('Login_page.html',context_instance=RequestContext(request))
  return render_to_response('portal.html',content, context_instance=RequestContext(request))

@csrf_exempt
def profile_render(request):
  try:
      username = request.session['username']
      passwd = request.session['password']
      desig = request.session['desig']
      content = {};
      query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
      print query
      from django.db import connection
      with connection.cursor() as cursor:
        cursor.execute(query)
        all_data = cursor.fetchall()
        print all_data
        if not all_data:
            return render_to_response('Login_page.html',context_instance=RequestContext(request))
        col_name_list = [desc[0] for desc in cursor.description]
        user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
        year = datetime.date.today().year
        post = request.GET.get('desig')
        query = 'select * from Election_citizens as ct inner join Election_candidates as c on ct.user_name = c.user_name where year(c.candidature_date)="'+str(year)+'" and candidate_designation ="'+str(post.split('_')[0])+'";'
        profile_data=[]
        with connection.cursor() as cursor:
          cursor.execute(query)
          prof_data = cursor.fetchall()
          prof_col_name_list = [desc[0] for desc in cursor.description]
          profile_data=map(lambda z:dict(izip(prof_col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), prof_data))
        # content={}
        return render_to_response('profiles.html',{"data":profile_data}, context_instance=RequestContext(request))

  except:
        return render_to_response('Login_page.html',context_instance=RequestContext(request))

@csrf_exempt
def result_render(request):
  try:
      username = request.session['username']
      passwd = request.session['password']
      desig = request.session['desig']
  except:
        return render_to_response('Login_page.html',context_instance=RequestContext(request))

  query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
  print query
  from django.db import connection
  with connection.cursor() as cursor:
    cursor.execute(query)
    all_data = cursor.fetchall()
    print all_data
    if not all_data:
        return render_to_response('Login_page.html',context_instance=RequestContext(request))
    col_name_list = [desc[0] for desc in cursor.description]
    user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
    year = datetime.date.today().year
    query = 'select * from Election_citizens as ct inner join Election_candidates as c on ct.user_name = c.user_name inner join (select max(vote_count) as total_vote from Election_candidates group by candidate_designation) as e on e.total_vote= c.vote_count where year(c.candidature_date)="'+str(year)+'";'
    result_data=[]
    with connection.cursor() as cursor:
      cursor.execute(query)
      res_data = cursor.fetchall()
      res_col_name_list = [desc[0] for desc in cursor.description]
      result_data=map(lambda z:dict(izip(res_col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), res_data))
    content={"president":[],"vp":[],"cultural":[],"sports":[]}
    for row in result_data:
        content[row['candidate_designation']].append(row['First_name']+" "+row['Last_name']);
    return render_to_response('results.html',content, context_instance=RequestContext(request))


@csrf_exempt
def cast_vote_render(request):
  try:
    username = request.session['username']
    passwd = request.session['password']
    desig = request.session['desig']
  except:
      pass
  print request.session['username']
  query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
  from django.db import connection
  with connection.cursor() as cursor:
    cursor.execute(query)
    all_data = cursor.fetchall()
    # print all_data
    if not all_data:
        return render_to_response('Login_page.html',context_instance=RequestContext(request))
    col_name_list = [desc[0] for desc in cursor.description]
    user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
    year = datetime.date.today().year
    query = 'select * from Election_vote_casted where user_name = "'+str(user_data[0]['user_name'])+'" and year(casted_year)="'+str(year)+'"'
    with connection.cursor() as cursor:
      cursor.execute(query)
      casted_data = cursor.fetchall();
    if not casted_data:
        query = 'select * from Election_citizens as ct inner join Election_candidates as c on ct.user_name = c.user_name where year(c.candidature_date)="'+str(year)+'";'
        profile_data=[]
        with connection.cursor() as cursor:
          cursor.execute(query)
          prof_data = cursor.fetchall()
          prof_col_name_list = [desc[0] for desc in cursor.description]
          profile_data=map(lambda z:dict(izip(prof_col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), prof_data))
        content={"president":[],"vp":[],"cultural":[],"sports":[]}
        for data in profile_data:
          content[data['candidate_designation']].append({"name":data['First_name']+" "+data['Last_name'],"user_name":data["user_name"]})
        print content
        return render_to_response('vote.html',{"data":content}, context_instance=RequestContext(request))

    else:
     return  HttpResponse(portal_render(request));

@csrf_exempt
def logout(request):
    try:
      del request.session['username']
      del request.session['password']
      del request.session['desig']
    except:
      pass
    return render_to_response('Login_page.html',context_instance=RequestContext(request))
@csrf_exempt
def confirm_vote(request):
    selected_ids = [str(itm) for itm in json.loads(request.POST.get('user_id'))] if request.POST.get('user_id') else [];
    try:
      username = request.session['username']
      passwd = request.session['password']
      desig = request.session['desig']
    except:
        pass
    query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
    from django.db import connection
    with connection.cursor() as cursor:
      cursor.execute(query)
      all_data = cursor.fetchall()
      # print all_data
      if not all_data:
          return render_to_response('Login_page.html',context_instance=RequestContext(request))
      col_name_list = [desc[0] for desc in cursor.description]
      user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
      year = datetime.date.today().year
      query = 'select * from Election_vote_casted where user_name = "'+str(user_data[0]['user_name'])+'" and year(casted_year)="'+str(year)+'"'
      with connection.cursor() as cursor:
        cursor.execute(query)
        casted_data = cursor.fetchall();
      if casted_data:
        return  HttpResponse(json.dumps({"success":False}));
      query = 'update Election_candidates set vote_count=vote_count+1 where user_name in ('+str(selected_ids)[1:-1]+') and year(candidature_date) ="'+str(year)+'";'
      try:
          with connection.cursor() as cursor:
              cursor.execute(query)
          query = 'insert into Election_vote_casted values("'+str(all_data[0][0])+'" ,"' +datetime.date.today().strftime("%Y-%m-%d")+'")';
          with connection.cursor() as cursor:
              cursor.execute(query)
          return HttpResponse(json.dumps({"success":True}));
      except:
          return HttpResponse(json.dumps({"success":False}));

@csrf_exempt
def delete_render(request):
  try:
    username = request.session['username']
    passwd = request.session['password']
    desig = request.session['desig']
  except:
      pass
  print request.session['username']
  query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
  from django.db import connection
  with connection.cursor() as cursor:
    cursor.execute(query)
    all_data = cursor.fetchall()
    # print all_data
    if not all_data:
        return render_to_response('Login_page.html',context_instance=RequestContext(request))
    col_name_list = [desc[0] for desc in cursor.description]
    user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
    year = datetime.date.today().year
    query = 'select * from Election_vote_casted where user_name = "'+str(user_data[0]['user_name'])+'" and year(casted_year)="'+str(year)+'"'
    with connection.cursor() as cursor:
      cursor.execute(query)
      casted_data = cursor.fetchall();
    query = 'select * from Election_citizens as ct inner join Election_candidates as c on ct.user_name = c.user_name where year(c.candidature_date)="'+str(year)+'";'
    profile_data=[]
    with connection.cursor() as cursor:
      cursor.execute(query)
      prof_data = cursor.fetchall()
      prof_col_name_list = [desc[0] for desc in cursor.description]
      profile_data=map(lambda z:dict(izip(prof_col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), prof_data))
    content={"president":[],"vp":[],"cultural":[],"sports":[]}
    for data in profile_data:
      content[data['candidate_designation']].append({"name":data['First_name']+" "+data['Last_name'],"user_name":data["user_name"]})
    return render_to_response('delete_candidates.html',{"data":content}, context_instance=RequestContext(request))
@csrf_exempt
def confirm_discard(request):
    selected_ids = [str(itm) for itm in json.loads(request.POST.get('user_id'))] if request.POST.get('user_id') else [];
    try:
      username = request.session['username']
      passwd = request.session['password']
      desig = request.session['desig']
    except:
        pass
    query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
    from django.db import connection
    with connection.cursor() as cursor:
      cursor.execute(query)
      all_data = cursor.fetchall()
      # print all_data
      if not all_data:
          return render_to_response('Login_page.html',context_instance=RequestContext(request))
      col_name_list = [desc[0] for desc in cursor.description]
      user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
      year = datetime.date.today().year
      query = 'delete from Election_candidates where user_name in ('+str(selected_ids)[1:-1]+') and year(candidature_date) ="'+str(year)+'";'
      try:
          with connection.cursor() as cursor:
              cursor.execute(query)
          return HttpResponse(json.dumps({"success":True}));
      except:
          return HttpResponse(json.dumps({"success":False}));

@csrf_exempt
def enroll_candidate(request):
    selected_ids = [str(itm) for itm in json.loads(request.POST.get('user_id'))] if request.POST.get('user_id') else [];
    try:
      username = request.session['username']
      passwd = request.session['password']
      desig = request.session['desig']
    except:
        pass
    query = 'select * from Election_login_data where email ="'+str(username)+'" and password ="'+str(passwd)+'";'
    from django.db import connection
    with connection.cursor() as cursor:
      cursor.execute(query)
      all_data = cursor.fetchall()
      # print all_data
      if not all_data:
          return render_to_response('Login_page.html',context_instance=RequestContext(request))
      col_name_list = [desc[0] for desc in cursor.description]
      user_data=map(lambda z:dict(izip(col_name_list,z)),map(lambda x:map(lambda y:smart_str(y),list(x)), all_data))
      year = datetime.date.today().year
      roll = request.POST.get("user")
      post = request.POST.get("post")
      agenda = request.POST.get("agenda")
      query = 'select * from Election_candidates where user_name = "'+str(roll)+'" and year(candidature_date)="'+str(year)+'"'
      with connection.cursor() as cursor:
        cursor.execute(query)
        casted_data = cursor.fetchall();
      if casted_data:
        return  HttpResponse(json.dumps({"success":False,"able":True}));
      query = 'select * from Election_citizens where user_name = "'+str(roll)+'";'
      print query
      with connection.cursor() as cursor:
        cursor.execute(query)
        citizen_data = cursor.fetchall();
      if not citizen_data:
        return  HttpResponse(json.dumps({"success":False,"athourized":True}));
      query = 'insert into Election_candidates values("'+str(roll)+'",0,"'+str(datetime.date.today().strftime("%Y-%m-%d"))+'","'+str(agenda)+'","'+str(post)+'");'
      try:
          with connection.cursor() as cursor:
              cursor.execute(query)
          return HttpResponse(json.dumps({"success":True}));
      except:
          return HttpResponse(json.dumps({"success":False}));
