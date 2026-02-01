import { useEffect, useState } from 'react';
import Header from '../../components/Header';
import { useParams } from 'react-router-dom';
import { GetStoryById, UpdateStory } from '../../endpoints/Stories';
import ManagePage from '../../components/writing/ManagePage';
import DeleteStoryPopup from '../../components/popups/DeleteStoryPopup';

function ManageStory({reload, setReload, setPopup, setPopupContent}) {
  const {id: storyId} = useParams();

    const [storyData, setStoryData] = useState("");
    const [editing, setEditing] = useState(false);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [sensitiveContent, setSensitiveContent] = useState(false);
    const [errText, setErrText] = useState(false);

    useEffect(() => {
        if (!storyId) return;

        const fetchStoryData = async () => {
            const preexistingData = await GetStoryById(storyId);
            setStoryData(preexistingData);
            setTitle(preexistingData.title);
            setDescription(preexistingData.description);
            setSensitiveContent(preexistingData.sensitiveContent);
        };
        fetchStoryData();
    }, [storyId, reload]);

    useEffect(() => {
        const updateErrText = () => {
            setErrText("")
        }
        updateErrText()
    }, [description, title]);

    async function UpdateStoryInfo(){
        if(!title || !description){
            setErrText("Please fill all fields.")
            return
        }
        await UpdateStory(storyId, title, description, sensitiveContent)
        setEditing(false)
        setReload(prev => !prev);
    }

    return (
        <>
            <Header/>
            <div className='px-[50px] divide-y-2 divide-[#D0D0D0] dark:divide-black'>
                <div className='flex flex-col items-center'>
                    {
                        editing ? 
                        <>
                            <div className='w-full'>
                                <p className='text-black dark:text-white'>Sensitive Content</p>
                                <label className={`relative inline-block w-11 h-6 cursor-pointer`}>
                                    <input
                                    type="checkbox"
                                    className="peer sr-only"
                                    onChange={(e) => setSensitiveContent(e.target.checked)}
                                    checked={sensitiveContent}
                                    />
                                    <span className="absolute inset-0 bg-gray-200 rounded-full transition-colors duration-200 ease-in-out dark:bg-[#D0D0D0] peer-checked:bg-[#0096FF] dark:peer-checked:bg-[#0065AD] peer-disabled:opacity-50 peer-disabled:pointer-events-none"></span>
                                    <span className="absolute top-1/2 start-0.5 -translate-y-1/2 size-5 bg-white rounded-full shadow-xs transition-transform duration-200 ease-in-out peer-checked:translate-x-full"></span>
                                </label>
                            </div>
                            <div className='w-full'>
                                <p className='text-black dark:text-white'>Title</p>
                                <input
                                    placeholder='Title...'
                                    value={title}
                                    className='w-full h-[40px] border-2 rounded-[15px] p-[10px] border-[#D0D0D0] dark:border-black bg-[#F4F4F4] dark:bg-[#292929] text-black dark:text-white'
                                    type="text" 
                                    onChange={(e) => setTitle(e.target.value)}
                                />
                            </div>

                            <div className='w-full'>
                                <p className='text-black dark:text-white'>Description</p>
                                <textarea
                                    placeholder='Description...'
                                    value={description}
                                    className='w-full h-[50px] min-h-[50px] border-2 rounded-[15px] p-[10px] border-[#D0D0D0] dark:border-black bg-[#F4F4F4] dark:bg-[#292929] text-black dark:text-white'
                                    onChange={(e) => setDescription(e.target.value)}
                                />
                            </div>
                        </>
                        :
                        <>
                            <p className='text-[25px] text-black dark:text-white mb-[5px]'>{storyData.title}</p>
                            <p className='text-black dark:text-white'>{storyData.description}</p>
                        </>
                    }
                    <p className="text-[#DF121B]">{errText}</p>
                    <div className="flex flex-col md:flex-row md:w-[400px] justify-between md:mt-[20px] mb-[20px]">
                        {
                            editing ?
                            <button
                                className="w-[150px] h-[40px] rounded-[15px] mt-[20px] md:mt-[0] text-white bg-[#0096FF] dark:bg-[#0065AD]"
                                onClick={() => UpdateStoryInfo()}
                            >save</button>
                            :
                            <button
                                className="w-[150px] h-[40px] rounded-[15px] mt-[20px] md:mt-[0] text-white bg-[#0096FF] dark:bg-[#0065AD]"
                                onClick={() => setEditing(true)}
                            >Edit Story Info</button>
                        }
                        <button
                            className="w-[150px] h-[40px] border-2 rounded-[15px] border-[#D0D0D0] dark:border-black bg-white dark:bg-[#171717] text-black dark:text-white md:mt-0 mt-[20px]"
                            onClick={() => {setPopupContent(
                            <DeleteStoryPopup
                                setReload={setReload}
                                setPopup={setPopup}
                                storyId={storyId}
                            />
                            ), setPopup(true)}}
                        >Delete Story</button>
                    </div>
                </div>
                <ManagePage
                    storyId={storyId}
                    reload={reload}
                    setReload={setReload}
                    setPopup={setPopup}
                    setPopupContent={setPopupContent}
                />
            </div>            
        </>
    )
}

export default ManageStory
