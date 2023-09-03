import { useState, useRef } from 'react';
import Modifier from './components/Modifier';
import axios from 'axios';
import './App.scss';

const App = () => {
  const oszUploadRef = useRef(null);
  const [difficulties, setDifficulties] = useState([]);
  const [isDifficultiesLoaded, setIsDifficultiesLoaded] = useState(false);
  const [isDifficultySelected, setIsDifficultySelected] = useState(false);
  const [difficultySettings, setDifficultySettings] = useState({});
  const [selectedDifficulty, setSelectedDifficulty] = useState([]);
  const [fileId, setFileId] = useState(null);

  const handleOszUpload = async (e) => {
    e.preventDefault()

    const file = oszUploadRef.current.files[0]
    const formFile = new FormData();

    formFile.append('osz', file)

    if (!file)
      return;

    console.log('Status: uploading osz file');
    const response = await axios
      .post('http://localhost:5000/osz-upload', formFile, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

    const responseData = response.data;
    
    if (responseData.fstatus > 0) {
      console.log('Status: osz file upload is unsuccessful');
      return;
    }

    setFileId(responseData.fid);
    setDifficulties(responseData.fdata);
    setIsDifficultiesLoaded(true);
  }

  const handleDifficultySelect = (index) => {
    setSelectedDifficulty(index);
  }

  const handleDifficultyUpload = async () => {
    const response = await axios
      .post('http://localhost:5000/difficulty-select', 
      {
        'fid': fileId,
        'fdata': difficulties[selectedDifficulty],
      }, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

    const responseData = response.data;

    if (responseData.fstatus > 0) {
      console.log('Status: osz parsing is unsuccessful');
      return;
    }

    setIsDifficultySelected(true);
    setDifficultySettings(responseData.fdata);
  }

  return (
    <div className="app">
      <h1 className="app-title">osu! Beatmap Tuner</h1>
      <form className="osz-form">
        <input type="file" className="osz-upload" ref={oszUploadRef} />
        <input type="submit" className="osz-upload-submit btn" onClick={e => handleOszUpload(e)}/>
      </form>

      {
        isDifficultiesLoaded &&
        (
          <div className="difficulty-selector">
            {difficulties.map((difficulty, index) => (
              <div 
                className={`difficulty diff-${index + 1}`} 
                key={index} 
                onClick={() => handleDifficultySelect(index)}
              >
                <h6>{difficulty}</h6>
              </div>
            ))}

            <button className="difficulty-button btn" onClick={() => handleDifficultyUpload()}>Select</button>     
          </div>
        )
      }

      {
        isDifficultySelected &&
        (
          <Modifier settings={difficultySettings}/>
        )
      }

      <div className="tuner">
      </div>
    </div>
  );
}

export default App;
