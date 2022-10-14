 if package_type == 'all_access_sub':
    sub_package = ProSubscriptionPackage.objects.get(stripe_product_id=request.data['stripe_product_id'])
    user = User.objects.get(email=request.data['user_email'])
    employer_profile = EmployerProfile.objects.get(user=user)

    if employer_profile.stripe_customer_id is None:
        user_full_name = f'{user.first_name} {user.last_name}'
        customer = stripe.Customer.create(
            email=request.data['user_email'],
            name=user_full_name
        )
    
    if employer_profile.stripe_customer_id:
        customer = stripe.Customer.retrieve(employer_profile.stripe_customer_id)

    # TODO: add receipt_email=user.email, on PROD

    if employer_profile.stripe_subscription_id is None:
        subscription = stripe.Subscription.create(
                customer=customer['id'],
                items=[{
                    'price': sub_package.stripe_price_id,
                }],
                payment_behavior='default_incomplete',
                expand=['latest_invoice.payment_intent'],
            )

        employer_profile.stripe_customer_id = subscription['customer']
        employer_profile.stripe_subscription_id = subscription['id']
        employer_profile.save()

        return Response({
            'client_secret': subscription['latest_invoice']['payment_intent']['client_secret']
        })
