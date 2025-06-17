/*product_list */

/*Btns color choices*/
const radioBtns = document.querySelectorAll('.product_card__btn-radio')  
radioBtns.forEach( radioBtn => {
    radioBtn.addEventListener("click", () => {
        let productCard  = radioBtn.parentElement.parentElement,
            productImg   = productCard.querySelector('.product_card__img > img'),
            productLink  = productCard.querySelector('.image_card'),
            proRadioBtns = productCard.querySelectorAll('.product_card__btn-radio')
        
        const cardPrice     = productCard.querySelector('.product_card__price')
        const originalPrice = cardPrice.querySelector(".original_price");
        const salePrice     = cardPrice.querySelector(".sale_price");

        const sp = radioBtn.dataset.sale_price     /**sale price data */
        const op = radioBtn.dataset.original_price /**original price data */
        const url = radioBtn.dataset.variation_id

        /*change dynamically the id in cart btn*/
        const link_cart = productCard.querySelector(".product_card__btn.cart")
        link_cart.dataset.variation_id = url
        link_cart.href = `/cart/add/${url}/`

        if(productLink.href != ''){
            productLink.href = ''
            productLink.href = `/product/${url}/`
        }

        if(sp === op){
            cardPrice.textContent = `$${op}`
        }else{
            cardPrice.innerHTML = `
                    <span class="original_price">$${op}</span>
                    <span class="sale_price">$${sp}</span>
            `
        }
        

        if (radioBtn.parentElement.parentElement === productCard){
            proRadioBtns.forEach(btn => btn.classList.remove("selected"))
            radioBtn.classList.add('selected')
            productImg.src = radioBtn.dataset.img
        }
        
        toggleActiveCartButtons()
    })

})

const spans = document.querySelectorAll('.color_choices')
spans.forEach(span=>{
    span.style.backgroundColor = span.dataset.bg_color
})



const link_cart = document.querySelectorAll(".product_card__btn.cart")
link_cart.forEach(link=>{
    const dataset = link.dataset.variation_id
    link.href = `/cart/add/${dataset}/`
})

/**check wich product is already added in cart */
function toggleActiveCartButtons() {
    const keys = document.querySelector('.most_popular_products').dataset.keys;
    console.log(keys);
    
    const cartButtons = document.querySelectorAll(".product_card__btn.cart");
    cartButtons.forEach(cartbtn => {
        const variation_id = cartbtn.dataset.variation_id;
        if (keys.includes(variation_id)) {
            cartbtn.classList.add('active');
        } else {
            cartbtn.classList.remove('active');
        }

        cartbtn.dataset.tooltip = cartbtn.classList.contains("active")? "remove from cart": "add to cart";
    });
}
toggleActiveCartButtons()



/*Btns color choices*/
const AddCartBtns = document.querySelectorAll('.product_card__btn');

AddCartBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        btn.classList.toggle("active");

        const isFav = btn.classList.contains("fav");
        const isCart = btn.classList.contains("cart");

        if (isFav) {
            btn.dataset.tooltip = btn.classList.contains("active")? "remove from wishlist": "add to wishlist";
        }

        if (isCart) {
            btn.dataset.tooltip = btn.classList.contains("active")? "add to cart": "remove from cart";
        }
    });
});

/*product_list */