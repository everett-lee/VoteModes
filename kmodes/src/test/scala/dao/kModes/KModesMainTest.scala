package dao.kModes

import dao.kModes.KModesData.{MPs, centroids}
import kModes.{CentroidsHelperMain, KModesMain}
import model.MPDetails
import org.mockito.ArgumentMatchers.any
import org.mockito.MockitoSugar.{spy, when}
import org.scalatest.wordspec.AnyWordSpec

class KModesMainTest extends AnyWordSpec {
  // given
  val mockedCentroidsHelper = spy(new CentroidsHelperMain())
  when(mockedCentroidsHelper.initCentroids(any(), any()))
    .thenReturn(centroids) // initial centroids are random so must be mocked

  val kModes = KModesMain(mockedCentroidsHelper)

  "The kModes class" should {
    "Give the correct output" in {
      // when
      val result = kModes.compute(MPs)

      // then
      assert(result == Map(
        6 -> Vector(MPDetails(3, "Mason Mount", "Chael Sea"), MPDetails(6, "SP Morrissey", "Controversial")),
        7 -> Vector(MPDetails(0, "Mark E Smith", "The Fall"), MPDetails(2, "Mark K", "Sun Kil Moon"),
          MPDetails(5, "T Werner", "Just Wide"), MPDetails(7, "The last one", "Has band")),
        4 -> Vector(MPDetails(1, "Richard D James", "Aphex"), MPDetails(4, "A Allen", "Trimley"))
      ))
    }
  }

}
