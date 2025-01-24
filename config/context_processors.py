def user_groups_status(request):
    is_authenticated = request.user.is_authenticated
    return {
        'is_revision_technician': is_authenticated and request.user.groups.filter(name='RevisionTechnician').exists(),
        'is_company_user': is_authenticated and request.user.groups.filter(name='CompanyUser').exists(),
        'is_company_supervisor': is_authenticated and request.user.groups.filter(name='CompanySupervisor').exists(),
        'is_superuser': is_authenticated and request.user.is_superuser,
    }