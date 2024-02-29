export interface BirdSong {
  id: number;
  fileurl: string;
  common_name: string;
  scientific_name: string;
  distancia_con_vector: number;
}

export const useBirdsServices = () => {
  const searchForBirdSongs = async (
    file: File,
    radius: number = 0.5,
    signal?: AbortSignal
  ): Promise<BirdSong[]> => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("radius", radius.toString());

    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/search_for_songs`,
      {
        method: "POST",
        body: formData,
        signal,
      }
    );

    if (!response.ok) {
      console.log(response);
      throw new Error("Request could not be fullfilled");
    }

    const responseJson = await response.json();

    for (const item of responseJson) {
      if (item.distancia_con_vector)
        item.distancia_con_vector = Number(item.distancia_con_vector);
    }

    return responseJson;
  };

  const fetchBirdImages = async (
    birdName: string,
    signal?: AbortSignal
  ): Promise<string> => {
    const response = await fetch(
      `${
        import.meta.env.VITE_BACKEND_URL
      }/get_bird_images?bird_name=${encodeURI(birdName)}`,
      {
        signal,
      }
    );

    if (!response.ok) {
      console.log(response);
      throw new Error("Request could not be fullfilled");
    }

    const responseJson = await response.json();

    if (responseJson.hits && responseJson.hits.length) {
      return responseJson.hits[0].webformatURL;
    }

    throw new Error("Could not find an image");
  };

  return {
    searchForBirdSongs,
    fetchBirdImages,
  };
};
