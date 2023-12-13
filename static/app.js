function setBaseHtml() {
    let html = `
    <div class="container">
    <h1 class="text-center"> Cupcakes </h1>
    <br>
        <div class="row" id="row1">
        </div>
    
    <br>
    <div class="row">
    <div class="col-3"></div>
    <div class="col-6 text-center">
        <h3 class="text-center"> Add a cupcake </h3>
        <form class="w-100">
            <div class="w-100 d-flex flex-row">
                <label for="flavor" class="w-25">Flavor:</label>
                <input type="text" id="flavor" class="form-control w-75" required>
            </div>
            <div class="w-100 d-flex flex-row">
                <label for="size" class="w-25">Size:</label>
                <input type="text" id="size" class="form-control w-75" required>
            </div>
            <div class="w-100 d-flex flex-row">
                <label for="rating" class="w-25">Rating:</label>
                <input type="text" id="rating" class="form-control w-75" required>
            </div>
            <div class="w-100 d-flex flex-row">
                <label for="image" class="w-25">Image URL:</label>
                <input type="text" id="image" class="form-control w-75">
            </div>
            <br>
            <div class="d-flex w-100 justify-content-end">
            <button class="btn btn-success" id="create">Submit</button>
            <div>
        </form>
        </div>
        </div>
        <div class="col-3"></div>
    </div>
    `;
    $(html).appendTo(document.body)
}

async function showCupcakes() {
    const cupcakes = await Cupcake.fetchAllCupcakes()
    cupcakes.forEach((cupcake) => {
        cupcake.addToPage()
    })
}

async function createCupcake(evt) {
    evt.preventDefault();
    const flavor = $('#flavor').val();
    const size = $('#size').val();
    const rating = $('#rating').val();
    const image = $('#image').val();

    const cupcake = await Cupcake.createCupcakes(flavor, size, rating, image)

    resetForm()

    cupcake.addToPage()

}

$(document).on('click', '#create', createCupcake);


function resetForm() {
    const flavor = $('#flavor').val("");
    const size = $('#size').val("");
    const rating = $('#rating').val("");
    const image = $('#image').val("");
}

function deleteCupcake(evt) {

    let cupcakeId = parseInt(evt.target.offsetParent.dataset.id);
    let cupcake = cupcakeMap.get(cupcakeId);
    cupcake.delete()
}

$(document).on('click', '.delete', deleteCupcake)


setBaseHtml();
showCupcakes();