import { useState } from "react";
import FileUploadInput from "./FileUploadInput";
import { useIonLoading, useIonToast } from "@ionic/react";
import { BirdSong, useSearchForBirdSongs } from "../services/bird_song";
import BirdSongsList from "./BirdSongsList";

const getSearchRadius = () => {
  const searchRadius = window.localStorage.getItem("search_radius");

  if (!searchRadius || Number.isNaN(searchRadius)) {
    return 0.5;
  }

  return Number(searchRadius);
};

const SongSearchForm = () => {
  const [presentLoading, dismissLoading] = useIonLoading();
  const [presentToast] = useIonToast();
  const { searchForBirdSongs } = useSearchForBirdSongs();

  const [resultsFromApi, setResultsFromApi] = useState<BirdSong[]>();

  const onFileUpload = async (file: File) => {
    console.log("upload");
    presentLoading("Loading songs...");
    try {
      const songs = await searchForBirdSongs(file, getSearchRadius());

      setResultsFromApi(songs);
    } catch (error) {
      console.error(error);
      presentToast({
        id: "search-songs-error",
        color: "danger",
        message: "Error ocurred",
        duration: 3000,
        position: "top",
      });
    }
    dismissLoading();
  };

  let innerComponent = <FileUploadInput onFileUpload={onFileUpload} />;

  if (resultsFromApi)
    innerComponent = (
      <BirdSongsList
        onDismiss={() => setResultsFromApi(undefined)}
        birdSongs={resultsFromApi}
      />
    );

  return (
    <div
      style={{
        display: "grid",
        height: "100%",
        placeItems: "center",
        paddingBottom: "2rem",
      }}
    >
      <div
        style={{
          maxWidth: 1200,
        }}
      >
        {innerComponent}
      </div>
    </div>
  );
};

export default SongSearchForm;
