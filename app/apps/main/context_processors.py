def add_user_to_context(request): 
	return {'current_user': request.user}