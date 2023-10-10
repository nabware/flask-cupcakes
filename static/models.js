"use strict";

const BASE_URL = "http://localhost:5000";

/**
 * Cupcake: a single cupcake in the system
 */

class Cupcake {

  constructor({ id, flavor, size, rating, image_url }) {
    this.id = id;
    this.flavor = flavor;
    this.size = size;
    this.rating = rating;
    this.imageUrl = image_url;
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

/**
 * CupcakeList: an array of Cupcakes
 */

class CupcakeList {
  constructor(cupcakes) {
    this.cupcakes = cupcakes;
  }

  /**
 * Calls the API to get all the cupcakes.
 * Returns an instance of CupcakeList.
 */

  static async getCupcakes() {
    const response = await fetch(`${BASE_URL}/api/cupcakes`);
    const data = await response.json();

    const cupcakes = data.cupcakes.map(cupcake => new Cupcake(cupcake));

    return new CupcakeList(cupcakes);
  }

  /**
   * Takes cupcake form inputs {flavor, size, rating, image_url [optional]},
   * adds to database and cupcake list,
   * and returns cupcake instance.
   */

  async addCupcake(cupcake) {
    const options = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(cupcake)
    };
    const response = await fetch(`${BASE_URL}/api/cupcakes`, options);
    const data = await response.json();

    const newCupcake = new Cupcake(data.cupcake);
    this.cupcakes.unshift(newCupcake);

    return newCupcake;
  }

    /**
   * Takes cupcake id,
   * deletes from database and cupcake list,
   * and returns deleted cupcake id.
   */

  async deleteCupcake(cupcakeId) {
    const options = {
      method: 'DELETE'
    };
    const response = await fetch(
      `${BASE_URL}/api/cupcakes/${cupcakeId}`,
      options
    );
    const data = await response.json();

    this.cupcakes = this.cupcakes.filter(c => c.id !== data.deleted);

    return data.deleted;
  }
}