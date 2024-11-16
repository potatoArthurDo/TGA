from store.models import Product, Profile

class Cart():

    def __init__(self, request):
        self.session = request.session
		# Get request
        self.request = request
		# Get the current session key if it exists
        self.cart = self.session.get('session_key')

		#If the user is new, no session key!  Create one!
        if 'session_key' not in request.session:
            self.cart = self.session['session_key'] = {}

		# Make sure cart is available on all pages of site
        self.cart = self.cart
	
    def get_cart_key(self, product_id, color = None, size = None):
		#Generate a unique key for each product variant, using 'default' for None.
        return f"{product_id}_{color or 'default'}_{size or 'default'}"
	
    def _save_cart_to_profile(self):
        """Save the cart to the user's profile in the database."""
        current_user = Profile.objects.filter(user__id=self.request.user.id)
        carty = str(self.cart).replace("'", "\"")  # Convert to JSON-compatible format
        current_user.update(items_in_cart=carty)

    def db_add(self, product, quantity, color=None, size=None):
        cart_key = self.get_cart_key(product.id, color, size)
		#Logic
        if cart_key in self.cart:
            pass
        else:
            self.cart[cart_key] = {
				'product_id': product.id,
				'quantity': quantity,
				'color': color,
				'size': size
			}
        self.session.modified = True

		#Deal with logged in user
        if self.request.user.is_authenticated:
            self._save_cart_to_profile()


    def add(self, product, quantity, color=None, size=None):
        cart_key = self.get_cart_key(product.id, color, size)

        if cart_key in self.cart:
            self.cart[cart_key]['quantity'] += quantity
        else:
            self.cart[cart_key] = {
				'product_id': product.id,
				'quantity': quantity,
				'color': color,	
				'size': size
			}

        self.session.modified = True

        if self.request.user.is_authenticated:
            self._save_cart_to_profile()

    def update(self, product, quantity, color=None, size=None):
        cart_key = self.get_cart_key(product.id, color, size)

        if cart_key in self.cart:
            if quantity > 0:
                self.cart[cart_key]['quantity'] = quantity
				#Remove item if quality is set to 0
            else:
                del self.cart[cart_key] 

        self.session.modified = True

        if self.request.user.is_authenticated:
            self._save_cart_to_profile()

    def delete(self, product, color=None, size=None):
        cart_key = self.get_cart_key(product, color, size)

        if cart_key in self.cart:
            del self.cart[cart_key]

        self.session.modified = True

        if self.request.user.is_authenticated:
            self._save_cart_to_profile()

    def cart_total(self):
        total = 0
        for item in self.cart.values():
            if isinstance(item,dict) and 'product_id' in item:
                product = Product.objects.get(id=item['product_id'])
                item_total = product.price * item['quantity']
                total += item_total
            formatted_total = f"{total:,}".replace(",", ".")
        return formatted_total

    def __len__(self):
        """Return the number of unique items in the cart."""
        return len(self.cart)
	
    def get_prods(self):
        """Retrieve product details for all items in the cart."""
        product_ids = [item['product_id'] for item in self.cart.values() if isinstance(item, dict)]
        products = Product.objects.filter(id__in=product_ids)
        return products
	

    def get_quants(self):
        """Get quantities of all items in the cart."""
        quantities = self.cart
        return quantities
	
    #Get cart items
    def get_cart_items(self):
        items = []
        for key, value in self.cart.items():
            product_id = value['product_id']
            quantity = value['quantity']
            color = value['color']
            size = value['size']
            product = Product.objects.get(id=product_id)
            items.append({'product': product, 'quantity': quantity, 'color': color, 'size': size})
        return items
  
	
# class Cart():
# 	def __init__(self, request):
# 		self.session = request.session
# 		# Get request
# 		self.request = request
# 		# Get the current session key if it exists
# 		cart = self.session.get('session_key')

# 		# If the user is new, no session key!  Create one!
# 		if 'session_key' not in request.session:
# 			cart = self.session['session_key'] = {}


# 		# Make sure cart is available on all pages of site
# 		self.cart = cart

# 	def db_add(self, product, quantity):
# 		product_id = str(product)
# 		product_qty = str(quantity)
# 		# Logic
# 		if product_id in self.cart:
# 			pass
# 		else:
# 			#self.cart[product_id] = {'price': str(product.price)}
# 			self.cart[product_id] = int(product_qty)

# 		self.session.modified = True

# 		# Deal with logged in user
# 		if self.request.user.is_authenticated:
# 			# Get the current user profile
# 			current_user = Profile.objects.filter(user__id=self.request.user.id)
# 			# Convert {'3':1, '2':4} to {"3":1, "2":4}
# 			carty = str(self.cart)
# 			carty = carty.replace("\'", "\"")
# 			# Save carty to the Profile Model
# 			current_user.update(items_in_cart=str(carty))


# 	def add(self, product, quantity):
# 		product_id = str(product.id)
# 		product_qty = str(quantity)
# 		# Logic
# 		if product_id in self.cart:
# 			pass
# 		else:
# 			#self.cart[product_id] = {'price': str(product.price)}
# 			self.cart[product_id] = int(product_qty)

# 		self.session.modified = True

# 		# Deal with logged in user
# 		if self.request.user.is_authenticated:
# 			# Get the current user profile
# 			current_user = Profile.objects.filter(user__id=self.request.user.id)
# 			# Convert {'3':1, '2':4} to {"3":1, "2":4}
# 			carty = str(self.cart)
# 			carty = carty.replace("\'", "\"")
# 			# Save carty to the Profile Model
# 			current_user.update(items_in_cart=str(carty))

# 	def cart_total(self):
# 		# Get product IDS
# 		product_ids = self.cart.keys()
# 		# lookup those keys in our products database model
# 		products = Product.objects.filter(id__in=product_ids)
# 		# Get quantities
# 		quantities = self.cart
# 		# Start counting at 0
# 		total = 0
		
# 		for key, value in quantities.items():
# 			# Convert key string into into so we can do math
# 			key = int(key)
# 			for product in products:
# 				if product.id == key:
# 					if product.is_sale:
# 						total = total + (product.sale_price * value)
# 					else:
# 						total = total + (product.price * value)



# 		return total



# 	def __len__(self):
# 		return len(self.cart)

# 	def get_prods(self):
# 		# Get ids from cart
# 		product_ids = self.cart.keys()
# 		# Use ids to lookup products in database model
# 		products = Product.objects.filter(id__in=product_ids)

# 		# Return those looked up products
# 		return products

# 	def get_quants(self):
# 		quantities = self.cart
# 		return quantities

# 	def update(self, product, quantity):
# 		product_id = str(product)
# 		product_qty = int(quantity)

# 		# Get cart
# 		ourcart = self.cart
# 		# Update Dictionary/cart
# 		ourcart[product_id] = product_qty

# 		self.session.modified = True
	

# 		# Deal with logged in user
# 		if self.request.user.is_authenticated:
# 			# Get the current user profile
# 			current_user = Profile.objects.filter(user__id=self.request.user.id)
# 			# Convert {'3':1, '2':4} to {"3":1, "2":4}
# 			carty = str(self.cart)
# 			carty = carty.replace("\'", "\"")
# 			# Save carty to the Profile Model
# 			current_user.update(items_in_cart=str(carty))


# 		thing = self.cart
# 		return thing

# 	def delete(self, product):
# 		product_id = str(product)
# 		# Delete from dictionary/cart
# 		if product_id in self.cart:
# 			del self.cart[product_id]

# 		self.session.modified = True

# 		# Deal with logged in user
# 		if self.request.user.is_authenticated:
# 			# Get the current user profile
# 			current_user = Profile.objects.filter(user__id=self.request.user.id)
# 			# Convert {'3':1, '2':4} to {"3":1, "2":4}
# 			carty = str(self.cart)
# 			carty = carty.replace("\'", "\"")
# 			# Save carty to the Profile Model
# 			current_user.update(items_in_cart=str(carty))