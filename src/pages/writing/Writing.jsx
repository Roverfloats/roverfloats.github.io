import Header from '../../components/Header';
import WorldbuildingOverview from '../../components/writing/WorldbuildingOverview';

function Writing({allowSensitive}) {
  return (
    <>
        <Header/>
        <div className="w-full h-auto px-[50px]">
          <WorldbuildingOverview allowSensitive={allowSensitive}/>
        </div>
    </>

  )
}

export default Writing
