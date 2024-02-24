export interface BirdSong {
  id: number;
  fileurl: string;
  common_name: string;
  scientific_name: string;
  distancia_con_vector: number;
}

export const useSearchForBirdSongs = () => {
  const searchForBirdSongs = async (
    file: File,
    radius: number = 0.5
  ): Promise<BirdSong[]> => {
    await new Promise((resolve) => {
      setTimeout(resolve, 2000);
    });

    const formData = new FormData();
    formData.append("file", file);
    formData.append("radius", radius.toString());

    const response = await fetch(
      `${import.meta.env.VITE_BACKEND_URL}/search_for_songs`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      console.log();
      throw new Error("Request could not be fullfilled");
    }

    const responseJson = await response.json();

    for (const item of responseJson) {
      if (item.distancia_con_vector)
        item.distancia_con_vector = Number(item.distancia_con_vector);
    }

    return responseJson;
  };

  return {
    searchForBirdSongs,
  };
};
