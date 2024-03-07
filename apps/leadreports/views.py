from django.shortcuts import render
from django.db.models import Count, Q
from django.db.models.functions import TruncWeek
from datetime import datetime
from django.contrib.auth.models import User
from leads.models import Leads, Sources, LeadType, Stage
from product.models import Product




def types(request):
    flag = 0
    type_id = user_id = ""
    leads = Leads.objects.all()
    type_id = request.GET.get("type")
    user_id = request.GET.get("user")
    weekly_data = ""

    if user_id:
        flag = 1
        if user_id == "all":
            source_ids = Sources.objects.values_list("id", flat=True)
        else:
            # source_ids = Sources.objects.filter(lead_source_users__user_id=user_id).values_list("id", flat=True)
            source_ids = Sources.objects.filter(assign_user__id=user_id).values_list("id", flat=True)


        leads = leads.filter(lead_source_id__in=source_ids)

    if type_id:
        flag = 1
        if type_id == "all":
            leads = leads.filter(Q(lead_type_id__name="") | Q(lead_type_id__name=None))
        else:
            leads = leads.filter(lead_type_id=type_id)

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        flag = 1
        if not end_date:
            leads = leads.filter(created_at__date__gte=start_date)
        else:
            leads = leads.filter(created_at__date__range=[start_date, end_date])

    total_leads = converted_leads = conversion_percentage = 0

    if flag == 1:
        lead_counts = leads

        weekly_data = lead_counts.annotate(week=TruncWeek('created_at')).values('week').annotate(
            date_range=Count('created_at', trunc_week=1),
            total=Count("id")
        ).filter(created_at__year=datetime.now().year)

        total_leads = lead_counts.count()
        converted_leads = lead_counts.filter(lead_status_id=20).count()

        if total_leads > 0 and converted_leads > 0:
            conversion_percentage = (converted_leads / total_leads) * 100

    users = User.objects.filter(groups__isnull=True).order_by("-id").values("id", "username")
    lead_types = LeadType.objects.values("id", "name", "score_range")

    context = {
        "users": users,
        "lead_types": lead_types,
        "type_id": type_id,
        "user_id": user_id,
        "total_leads": total_leads,
        "converted_leads": converted_leads,
        "conversion_percentage": conversion_percentage,
        "start_date": start_date,
        "end_date": end_date,
        "weekly_data": weekly_data,
        "flag": flag,
    }

    return render(request, "lead_reports/types.html", context)





def products(request):
    flag = 0
    product_id = user_id = ""
    leads = Leads.objects.all()
    product_id = request.GET.get("type")
    user_id = request.GET.get("user")
    weekly_data = ""

    if user_id:
        flag = 1
        if user_id == "all":
            source_ids = Sources.objects.values_list("id", flat=True)
        else:
            # source_ids = Sources.objects.filter(lead_source_users__user_id=user_id).values_list("id", flat=True)
            source_ids = Sources.objects.filter(assign_user__id=user_id).values_list("id", flat=True)


        leads = leads.filter(lead_source_id__in=source_ids)

    if product_id:
        flag = 1
        if product_id == "all":
            leads = leads.filter(Q(product_id__name="") | Q(product_id__name=None))
        else:
            leads = leads.filter(product_id=product_id)

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        flag = 1
        if not end_date:
            leads = leads.filter(created_at__date__gte=start_date)
        else:
            leads = leads.filter(created_at__date__range=[start_date, end_date])

    total_leads = converted_leads = conversion_percentage = 0

    if flag == 1:
        lead_counts = leads

        weekly_data = lead_counts.annotate(week=TruncWeek('created_at')).values('week').annotate(
            date_range=Count('created_at', trunc_week=1),
            total=Count("id")
        ).filter(created_at__year=datetime.now().year)

        total_leads = lead_counts.count()
        converted_leads = lead_counts.filter(lead_status_id=20).count()

        if total_leads > 0 and converted_leads > 0:
            conversion_percentage = (converted_leads / total_leads) * 100

    users = User.objects.filter(groups__isnull=True).order_by("-id").values("id", "username")
    product_types = Product.objects.values("id", "name")



    context = {
        "users": users,
        "product_types": product_types,
        "product_id": product_id,
        "user_id": user_id,
        "total_leads": total_leads,
        "converted_leads": converted_leads,
        "conversion_percentage": conversion_percentage,
        "start_date": start_date,
        "end_date": end_date,
        "weekly_data": weekly_data,
        "flag": flag,
    }

    return render(request, "lead_reports/products.html", context)



def sources(request):
    flag = 0
    source_id = user_id = ""
    leads = Leads.objects.all()
    source_id = request.GET.get("type")
    user_id = request.GET.get("user")
    weekly_data = ""

    if user_id:
        flag = 1
        if user_id == "all":
            source_ids = Sources.objects.values_list("id", flat=True)
        else:
            # source_ids = Sources.objects.filter(lead_source_users__user_id=user_id).values_list("id", flat=True)
            source_ids = Sources.objects.filter(assign_user__id=user_id).values_list("id", flat=True)


        leads = leads.filter(lead_source_id__in=source_ids)

    if source_id:
        flag = 1
        if source_id == "all":
            leads = leads.filter(Q(lead_source_id__name="") | Q(lead_source_id__name=None))
        else:
            leads = leads.filter(lead_source_id=source_id)

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        flag = 1
        if not end_date:
            leads = leads.filter(created_at__date__gte=start_date)
        else:
            leads = leads.filter(created_at__date__range=[start_date, end_date])

    total_leads = converted_leads = conversion_percentage = 0

    if flag == 1:
        lead_counts = leads

        weekly_data = lead_counts.annotate(week=TruncWeek('created_at')).values('week').annotate(
            date_range=Count('created_at', trunc_week=1),
            total=Count("id")
        ).filter(created_at__year=datetime.now().year)

        total_leads = lead_counts.count()
        converted_leads = lead_counts.filter(lead_status_id=20).count()

        if total_leads > 0 and converted_leads > 0:
            conversion_percentage = (converted_leads / total_leads) * 100

    users = User.objects.filter(groups__isnull=True).order_by("-id").values("id", "username")
    source_types = Sources.objects.values("id", "name")

    context = {
        "users": users,
        "source_types": source_types,
        "source_id": source_id,
        "user_id": user_id,
        "total_leads": total_leads,
        "converted_leads": converted_leads,
        "conversion_percentage": conversion_percentage,
        "start_date": start_date,
        "end_date": end_date,
        "weekly_data": weekly_data,
        "flag": flag,
    }

    return render(request, "lead_reports/sources.html", context)



def stages(request):
    flag = 0
    stage_id = user_id = ""
    leads = Leads.objects.all()
    stage_id = request.GET.get("type")
    user_id = request.GET.get("user")
    weekly_data = ""

    if user_id:
        flag = 1
        if user_id == "all":
            source_ids = Sources.objects.values_list("id", flat=True)
        else:
            # source_ids = Sources.objects.filter(lead_source_users__user_id=user_id).values_list("id", flat=True)
            source_ids = Sources.objects.filter(assign_user__id=user_id).values_list("id", flat=True)


        leads = leads.filter(lead_source_id__in=source_ids)

    if stage_id:
        flag = 1
        if stage_id == "all":
            leads = leads.filter(Q(lead_status_id__name="") | Q(lead_status_id__name=None))
        else:
            leads = leads.filter(lead_status_id=stage_id)

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        flag = 1
        if not end_date:
            leads = leads.filter(created_at__date__gte=start_date)
        else:
            leads = leads.filter(created_at__date__range=[start_date, end_date])

    total_leads = converted_leads = conversion_percentage = 0

    if flag == 1:
        lead_counts = leads

        weekly_data = lead_counts.annotate(week=TruncWeek('created_at')).values('week').annotate(
            date_range=Count('created_at', trunc_week=1),
            total=Count("id")
        ).filter(created_at__year=datetime.now().year)

        total_leads = lead_counts.count()
        converted_leads = lead_counts.filter(lead_status_id=20).count()

        if total_leads > 0 and converted_leads > 0:
            conversion_percentage = (converted_leads / total_leads) * 100

    users = User.objects.filter(groups__isnull=True).order_by("-id").values("id", "username")
    lead_stage = Stage.objects.values("id", "name")

    context = {
        "users": users,
        "lead_stage": lead_stage,
        "stage_id": stage_id,
        "user_id": user_id,
        "total_leads": total_leads,
        "converted_leads": converted_leads,
        "conversion_percentage": conversion_percentage,
        "start_date": start_date,
        "end_date": end_date,
        "weekly_data": weekly_data,
        "flag": flag,
    }

    return render(request, "lead_reports/stages.html", context)



    # flag = 0
    # product_id = user_id = ""
    # leads = Leads.objects.all()
    # product_id = request.GET.get("type")
    # user_id = request.GET.get("user")
    # weekly_data = ""

    # if user_id:
    #     flag = 1
    #     if user_id == "all":
    #         source_ids = Sources.objects.values_list("id", flat=True)
    #     else:
    #         source_ids = Sources.objects.filter(lead_source_users__user_id=user_id).values_list("id", flat=True)

    #     leads = leads.filter(lead_source_id__in=source_ids)

    # if product_id:
    #     flag = 1
    #     if product_id == "all":
    #         leads = leads.filter(Q(lead_product_id="") | Q(lead_product_id=None))
    #     else:
    #         leads = leads.filter(lead_product_id=product_id)

    # start_date = request.GET.get("start_date")
    # end_date = request.GET.get("end_date")

    # if start_date:
    #     flag = 1
    #     if not end_date:
    #         leads = leads.filter(created_at__date__gte=start_date)
    #     else:
    #         leads = leads.filter(created_at__date__range=[start_date, end_date])

    # total_leads = converted_leads = conversion_percentage = 0

    # if flag == 1:
    #     lead_counts = leads

    #     weekly_data = lead_counts.values(week=F("created_at__week")).annotate(
    #         date_range=Count("created_at__week", Week=1),
    #         total=Count("id")
    #     ).filter(created_at__year=datetime.now().year)

    #     total_leads = lead_counts.count()
    #     converted_leads = lead_counts.filter(lead_status_id=20).count()

    #     if total_leads > 0 and converted_leads > 0:
    #         conversion_percentage = (converted_leads / total_leads) * 100

    # users = User.objects.filter(role__isnull=True).order_by("-id").values("id", "name")
    # lead_types = LeadType.objects.values("id", "name")

    # context = {
    #     "users": users,
    #     "lead_types": lead_types,
    #     "product_id": product_id,
    #     "user_id": user_id,
    #     "total_leads": total_leads,
    #     "converted_leads": converted_leads,
    #     "conversion_percentage": conversion_percentage,
    #     "start_date": start_date,
    #     "end_date": end_date,
    #     "weekly_data": weekly_data,
    #     "flag": flag,
    # }

    # return render(request, "lead_reports/types.html", context)
