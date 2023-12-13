let cupcakeMap = new Map();

class Cupcake {

    constructor(cupcake) {
        this.id = cupcake.id;
        this.flavor = cupcake.flavor;
        this.size = cupcake.size;
        this.rating = cupcake.rating;
        this.image = cupcake.image;

    }

    static async fetchAllCupcakes() {
        const req = await axios.get("/api/cupcakes")
        const cupcakes = []
        req.data["cupcakes"].forEach((item) => {
            const new_cupcake = new Cupcake(item)
            cupcakeMap.set(new_cupcake.id, new_cupcake)
            cupcakes.push(new_cupcake)
        })

        return cupcakes
    }

    static async createCupcakes(flavor, size, rating, image) {

        const data = { "flavor": flavor, "size": size, "rating": rating, "image": image }
        if (image === "") {
            data.image = "https://tinyurl.com/demo-cupcake"
        }

        const resp = await axios.post('/api/cupcakes', data)

        const cupcake = new Cupcake(resp.data.cupcake);
        cupcakeMap.set(cupcake.id, cupcake)
        return cupcake
    }

    addToPage() {
        let html = `
        <div class="col-3" id=${this.id}>
            <div class="card" style="width: 18rem;" data-id="${this.id}">
                <img class="card-img-top" src="${this.image}" alt="Card image cap">
                <div class="card-body">
                <ul class="list-group list-group-flush">
                    <li class="list-group-item">Flavor: ${this.flavor}</li>
                 <li class="list-group-item">Rating: ${this.rating}</li>
                    <li class="list-group-item">Size: ${this.size}</li>
                </ul>   
                </div>
                <div class="text-center">
                <small><button class="btn btn-danger delete" id="btn${this.id}">X</button></small>
                <div>
            </div>
        </div>
        `;
        $('#row1').append(html)
    }

    async delete() {
        const resp = await axios.delete(`/api/cupcakes/${this.id}`)

        if (resp.data.message === "Deleted") {
            $(`#${this.id}`).remove()
            cupcakeMap.delete(this.id)
        }
        else {
            alert("Cupcake failed to delete")
        }
    }


}