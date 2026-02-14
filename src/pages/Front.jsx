import Header from '../components/Header';
import RecurringTaskOverview from '../components/tasks/RecurringTaskOverview';
import TaskOverview from '../components/tasks/TaskOverview copy';

function Front({reload, setReload, setPopup, setPopupContent}) {

  return (
    <>
        <Header/>
        <div className="w-full h-auto grid grid-cols-1 md:grid-cols-2 divide-solid divide-y-2 md:divide-x-2 md:divide-y-0 divide-[#D0D0D0] dark:divide-[black]">
            <RecurringTaskOverview
              setReload={setReload}
              reload={reload}
              setPopup={setPopup}
              setPopupContent={setPopupContent}
            />
            <TaskOverview
              setReload={setReload}
              reload={reload}
              setPopup={setPopup}
              setPopupContent={setPopupContent}
            />
          <div className='md:col-span-2'></div>
        </div>

    </>

  )
}

export default Front
