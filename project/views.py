from django.shortcuts import render,redirect
import hashlib
from . import models
from django.http import HttpResponse, HttpResponseRedirect,FileResponse,Http404, JsonResponse
from FBA import settings
import csv
import re
from .FBA_LNA import run
from .cycle import draw_cycle,del_file,to_file
import pandas as pd
import os
import ast
from django.views.decorators.csrf import csrf_exempt
import json
from django.core.paginator import Paginator

def webApp(request):
    try:
        return render(request,'webApp.html')
    except:
        return render(request,"error.html")

def webAppcont(request):
    try:
        model_input = request.FILES.get('model_input') 
        illumination = float(request.POST.get("growcondition"))
        h = float(request.POST.get("h"))
        h2o = float(request.POST.get("h2o"))
        pi = float(request.POST.get("pi"))
        nh4 = float(request.POST.get("nh4")) 
        no3 = float(request.POST.get("no3"))
        so4 = float(request.POST.get("so4")) 
        o2 = float(request.POST.get("o2"))
        ac = float(request.POST.get("ac")) 
        # 加密
        string = str(model_input) + "-" + str(illumination) + "-" + str(h) + "-" + str(h2o) + "-" + str(pi) + "-" + str(nh4) + "-" + str(no3) + "-" + str(so4) + "-" + str(o2) + "-" + str(ac)
        md5 = hashlib.md5()
        md5.update(bytes(string,encoding="utf-8"))
        hash_str = md5.hexdigest()
        # 判断之前是否传输过相同的文件和条件
        file_exist = models.File.objects.filter(hash_str=hash_str)
        if not file_exist.exists():
            models.File.objects.create(title=model_input,illumination=illumination,h=h,h2o=h2o,pi=pi,nh4=nh4,no3=no3,so4=so4,o2=o2,ac=ac,hash_str=hash_str)  

        return HttpResponseRedirect('/download/'+hash_str)

    except:
        return render(request,"error.html")

def download(request,hash_str):
    try:
        return render(request,'download.html',{'hash_str':hash_str})
    except:
        return render(request,"error.html")

def cont(request):
    try:
        fluxFile = request.POST.get("fluxes")
        hash_string = fluxFile[:32]
        format = fluxFile[32:]
        file = models.File.objects.get(hash_str=hash_string)
        model_input = file.title
        illumination = file.illumination
        h = file.h
        h2o = file.h2o
        pi = file.pi
        nh4 = file.nh4
        no3 = file.no3
        so4 = file.so4
        o2 = file.o2
        ac = file.ac

        if file.filetxt:
            if format == "fluxestxt":
                hash_name = hash_string + ".txt"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)        
            if format == "fluxescsv":
                hash_name = hash_string + ".csv"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
            if format == "fluxesReactioncsv_h":
                    hash_name = hash_string + "_h.csv"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
            if format == "fluxesReactioncsv_u":
                hash_name = hash_string + "_u.csv"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
            if format == "fluxesReactioncsv_m":
                hash_name = hash_string + "_m.csv"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
            if format == "fluxesReactioncsv_c":
                hash_name = hash_string + "_c.csv"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
            file_down = open(path,'rb')
            response = FileResponse(file_down)
            response['Content-Type']='application/octet-stream'
            response['Content-Disposition']='attachment;filename=%s'%hash_name
            return response
        else:
            DIR = settings.MEDIA_ROOT + "/download"
            dir = settings.MEDIA_ROOT + "/model"
            file_dir = [name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR,name))]          
            if len(file_dir) > 60:
                del_file(DIR)
                del_file(dir)
                models.File.objects.all().delete()

            result=run(model_input,illumination,h,h2o,pi,nh4,no3,so4,o2,ac)
            if type(result)==str:
                return render(request,'webApp.html',{'error_message':result})
            else:
                pFBA_status,obj_value,fluxes = result
                hash_name = hash_string + ".csv"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                with open(path,'w') as fcsv:
                    fcsv.write("pFBA status: "+str(pFBA_status)+"\n")
                    fcsv.write("pFBA solution: "+str(obj_value)+"\n")
                    writer=csv.writer(fcsv)
                    writer.writerows(zip(fluxes.index,fluxes))

                hash_name = hash_string + ".txt"
                path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                f = open(path,'w')
                f.write("pFBA status: "+str(pFBA_status)+"\n")
                f.write("--"*30+"\n")
                f.write("pFBA solution: "+str(obj_value)+"\n")
                f.write("--"*30+"\n")
                for i in range(0,len(fluxes)):
                    f.write(fluxes.index[i]+" "*10+str(fluxes[i])+"\n")
                        
                path_now = os.getcwd()
                file1 = pd.read_csv(path_now + "/project/SBML_reactions_merged_gateways.csv")
                file2 = pd.read_csv(path_now + "/project/SBML_species.csv")
                file_new = pd.merge(file1,file2,on="species")

                fluxes.index = "R_" + fluxes.index
                fi = pd.DataFrame({"reaction":list(fluxes.index),'num':list(fluxes[:])})
                result = pd.merge(fi,file_new,on="reaction")
                result[["stoich"]] = result[["stoich"]].astype(str)
                result["values"] = result["num"] * result["mass"]
                result = result[abs(result["values"]) >= 10**(-6)]
                result["values"] = result["values"].map(lambda x: str(x))

                result_h = result[result["compartment"]=="h"]
                result_u = result[result["compartment"]=="u"]
                result_m = result[result["compartment"]=="m"]
                result_c = result[result["compartment"]=="c"]
                pro_sub_h = to_file(result_h)
                pro_sub_u = to_file(result_u)
                pro_sub_m = to_file(result_m)
                pro_sub_c = to_file(result_c)
                path_h = "%s/%s/%s" % (settings.MEDIA_ROOT,"download","%s_h.csv"%hash_string)
                path_u = "%s/%s/%s" % (settings.MEDIA_ROOT,"download","%s_u.csv"%hash_string)
                path_m = "%s/%s/%s" % (settings.MEDIA_ROOT,"download","%s_m.csv"%hash_string)
                path_c = "%s/%s/%s" % (settings.MEDIA_ROOT,"download","%s_c.csv"%hash_string)
                pro_sub_h.to_csv(path_h,index=False,header=False)
                pro_sub_u.to_csv(path_u,index=False,header=False)
                pro_sub_m.to_csv(path_m,index=False,header=False)
                pro_sub_c.to_csv(path_c,index=False,header=False)

                file.delete()
                models.File.objects.create(title=model_input,illumination=illumination,h=h,h2o=h2o,pi=pi,nh4=nh4,no3=no3,so4=so4,o2=o2,ac=ac,hash_str=hash_string,filetxt=hash_name)  
                
                if format == "fluxestxt":
                    hash_name = hash_string + ".txt"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                if format == "fluxescsv":
                    hash_name = hash_string + ".csv"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                if format == "fluxesReactioncsv_h":
                    hash_name = hash_string + "_h.csv"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                if format == "fluxesReactioncsv_u":
                    hash_name = hash_string + "_u.csv"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                if format == "fluxesReactioncsv_m":
                    hash_name = hash_string + "_m.csv"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                if format == "fluxesReactioncsv_c":
                    hash_name = hash_string + "_c.csv"
                    path = "%s/%s/%s" % (settings.MEDIA_ROOT,"download",hash_name)
                
                    
                file_down = open(path,'rb')
                response =FileResponse(file_down)
                response['Content-Type']='application/octet-stream'
                response['Content-Disposition']='attachment;filename=%s'%hash_name

                return response
    except:
        return render(request,"error.html")

def result(request):
    if request.method == "POST":
        cycle_file = request.FILES.get("file_input")

        md5 = hashlib.md5()
        md5.update(bytes(str(cycle_file),encoding="utf-8"))
        hash_str = md5.hexdigest()

        cyclefile = models.Cycle.objects.filter(hash_str=hash_str)
        if not cyclefile.exists():
            models.Cycle.objects.create(title=cycle_file,hash_str=hash_str)
        return HttpResponseRedirect("/resultcont/"+hash_str)

    return render(request,"result.html")

def resultcont(request,hash_str):
    try:
        cycle_file = models.Cycle.objects.filter(hash_str=hash_str)
        if cycle_file.exists():
            cycle_file = models.Cycle.objects.get(hash_str=hash_str).title
        reactions = pd.read_table(cycle_file,header=None,names="A")
        num = []
        for index,row in reactions.iterrows():
            rea = row["A"]
            num.append(float((re.split('/',rea)[1])))
        reactions["B"] = num

        reactions.sort_values("B",ascending=False,inplace=True)
        reactions.reset_index(drop=True,inplace=True)

        cycles = list(reactions["A"])
        nums = list(reactions["B"])
        paginator_cycles = Paginator(cycles,20)
        paginator_nums = Paginator(nums,20)

        count = paginator_cycles.count
        page_num = paginator_cycles.num_pages
        page_range = paginator_cycles.page_range

        try:
            current_num = int(request.GET.get('page',1))
        except:
            current_num = 1
        # 不在页码范围内的安全处理，防止get请求时候
        if current_num < 1:
            current_num = 1
        if current_num > page_num:
            current_num = page_num

        cycle = paginator_cycles.page(current_num)
        num = paginator_nums.page(current_num)
        cycles_num = dict(zip(cycle,num))

        if page_num > 3:
            if current_num > 1 and current_num + 2 <= page_num + 1:
                page_range = range(current_num-1,current_num+2)
            elif current_num <=2:
                page_range = range(1,4)
            elif current_num + 2 > page_num + 1:
                page_range = range(page_num-2,page_num+1)

        return render(request,"result.html",locals())
    except:
        return render(request,"error.html")
    
@csrf_exempt
def view(request):
    try:
        dir = settings.MEDIA_ROOT + "/image"
        file_dir = [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir,name))]          
        if len(file_dir) > 80:
            del_file(dir)

        data = request.POST.get("cycle")
        image_name = draw_cycle(reaction=data)
        path = "%s/%s/%s"%(settings.MEDIA_URL,"image",image_name)
        context = {'path':path}
        return JsonResponse(context)
    except:
        return render(request,"error.html")

@csrf_exempt
def downloadimage(request):
    try:
        dir = settings.MEDIA_ROOT + "/image"
        file_dir = [name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir,name))]          
        if len(file_dir) > 80:
            del_file(dir)

        data = request.POST.get("cycle")
        image_name = draw_cycle(reaction=data)
        context = {"name":image_name}
        return JsonResponse(context)
    except:
        return render(request,"error.html")

def search(request,hash_str):
    try:
        return render(request,"search.html",{"hash_str":hash_str})
    except:
        return render(request,"error.html")

def searchcont(request):
    try:
        reaction_word = request.POST.get("reactionword")
        hash_str = request.POST.get("hash_str")
        cycle_file = models.Cycle.objects.filter(hash_str=hash_str)

        if cycle_file.exists():
            cycle_file = models.Cycle.objects.get(hash_str=hash_str).title
        reactions = pd.read_table(cycle_file,header=None,names="A")

        num = []
        for index,row in reactions.iterrows():
            rea = row["A"]
            num.append(float((re.split('/',rea)[1])))
        reactions["B"] = num

        reactions.sort_values("B",ascending=False,inplace=True)
        reactions.reset_index(drop=True,inplace=True)

        reaction_word_list = reaction_word.split(",")
        for i in reaction_word_list:
            reactions = reactions[reactions["A"].str.contains(i)]
        reactions_sub = reactions

        min_value = float(request.POST.get("min_value"))
        max_value = float(request.POST.get("max_value"))
        reactions_sub = reactions_sub[reactions_sub["B"]>=min_value][reactions_sub["B"]<=max_value]
        if reactions_sub.empty:
            search_result = "There are none cycles containing " + " and ".join(reaction_word_list) + " whose fluxes mass is between " + str(min_value) + " and " + str(max_value) + ". Please try again."
            return render(request,"search.html",{"search_result":search_result})
        else:
            search_num = len(reactions_sub)
            reactions_sub.sort_values("B",ascending=False,inplace=True)
            reactions_sub.reset_index(drop=True,inplace=True)
            cycles = list(reactions_sub["A"])
            nums = list(reactions_sub["B"]) 
            cycles_num = list(map(lambda x,y:[x,y],cycles,nums))
            cycle_list = []
            for i in cycles_num:
                cycle_list.append(models.Reactions(cycle=i[0],value=i[1]))
            models.Reactions.objects.all().delete()
            models.Reactions.objects.bulk_create(cycle_list)
            return redirect('/searchresult/'+ hash_str)
    except:
        return render(request,"error.html")

def searchresult(request,hash_str):
    try:
        cycle_list = models.Reactions.objects.all()
        cycles = []
        nums = []
        for i in range(len(cycle_list)):
            cycles.append(cycle_list[i].cycle)
            nums.append(cycle_list[i].value)
        search_num = len(nums)
        paginator_cycles = Paginator(cycles,20)
        paginator_nums = Paginator(nums,20)
        count = paginator_cycles.count
        page_num = paginator_cycles.num_pages
        page_range = paginator_cycles.page_range 
        try:
            current_num = int(request.GET.get('page',1))
        except:
            current_num = 1
    
        if current_num < 1:
            current_num = 1
        if current_num > page_num:
            current_num = page_num
        cycle = paginator_cycles.page(current_num)
        num = paginator_nums.page(current_num)
        s_cycles_num = dict(zip(cycle,num))
        search_result = "There are altogether " + str(search_num) +" cycles. "
        if page_num > 3:
            if current_num > 1 and current_num + 2 <= page_num + 1:
                page_range = range(current_num-1,current_num+2)
            elif current_num <=2:
                page_range = range(1,4)
            elif current_num + 2 > page_num + 1:
                page_range = range(page_num-2,page_num+1)
        return render(request,"search.html",locals())
    except:
        return render(request,"error.html")

def help(request):
    try:
        return render(request,"help.html")
    except:
        return render(request,"error.html")   






