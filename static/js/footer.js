/*Footer*/
const dropdown_content = document.querySelectorAll("footer .col h1")
dropdown_content.forEach(el =>{
    const dropdown = el.parentElement.querySelector('.dropdown')
    el.addEventListener('click', ()=>{
        dropdown.classList.toggle("active")
    })
})
/*Footer*/