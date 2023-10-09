"use strict";

const BASE_URL = "http://localhost";

/**
 * Cupcake: a single cupcake in the system
 */

class Cupcake {

  constructor({id, flavor, size, rating, image_url}) {
    this.id = id;
    this.flavor = flavor;
    this.size = size;
    this.rating = rating;
    this.image_url = image_url
  }

  /**
   * Calls the API to get a single cupcake.
   * Returns an instance of that cupcake.
   */
  static async getCupcake(cupcakeId) {
    const response = await fetch(`${BASE_URL}/api/cupcakes/${cupcakeId}`);
    const data = await response.json();
    return new Cupcake(data.cupcake);
  }
}