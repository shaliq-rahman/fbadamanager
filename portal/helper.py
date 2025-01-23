from django.shortcuts import render

def renderhelper(request, app_name, folder, template_name, context=None):
    """
    A helper function to render templates from a specified app and folder.

    Args:
        request: The HTTP request object.
        app_name (str): Name of the app (e.g., 'myapp').
        folder (str): Subfolder within the app's templates directory.
        template_name (str): Name of the HTML file to render.
        context (dict): Context data to pass to the template (default: None).

    Returns:
        HttpResponse: Rendered template response.
    """
    context = context or {}
    template_path = f"{app_name}/{folder}/{template_name}"
    return render(request, template_path, context)