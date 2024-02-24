export interface BirdSong {
  id: number;
  fileUrl: string;
  common_name: string;
  scientific_name: string;
  distancia_con_vector: number;
}

export const useSearchForBirdSongs = () => {
  const searchForBirdSongs = async (file: File) => {
    await new Promise((resolve) => {
      setTimeout(resolve, 2000);
    });

    const result: BirdSong[] = [
      {
        id: 1,
        fileUrl:
          "https://xeno-canto.org/sounds/uploaded/BTOFEKXFGW/XC198453-T10.mp3",
        common_name: "Ave 1",
        distancia_con_vector: 0.3,
        scientific_name: "sc1",
      },
      {
        id: 2,
        fileUrl:
          "https://xeno-canto.org/sounds/uploaded/BTOFEKXFGW/XC198453-T10.mp3",
        common_name: "Ave 2",
        distancia_con_vector: 0.3,
        scientific_name: "sc2",
      },
      {
        id: 3,
        fileUrl:
          "https://xeno-canto.org/sounds/uploaded/BTOFEKXFGW/XC198453-T10.mp3",
        common_name: "Ave 3",
        distancia_con_vector: 0.3,
        scientific_name: "sc3",
      },
      {
        id: 4,
        fileUrl:
          "https://xeno-canto.org/sounds/uploaded/BTOFEKXFGW/XC198453-T10.mp3",
        common_name: "Ave 4",
        distancia_con_vector: 0.3,
        scientific_name: "sc4",
      },
      {
        id: 5,
        fileUrl:
          "https://xeno-canto.org/sounds/uploaded/BTOFEKXFGW/XC198453-T10.mp3",
        common_name: "Ave 5",
        distancia_con_vector: 0.3,
        scientific_name: "sc5",
      },
    ];

    return result;
  };

  return {
    searchForBirdSongs,
  };
};
