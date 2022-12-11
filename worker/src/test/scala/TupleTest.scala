package test

import java.lang.IllegalArgumentException
import org.scalatest.funsuite.AnyFunSuite
import scala.io.Source

import worker.Tuple
import test.util._


class TupleSuite extends AnyFunSuite {

    loadPartition()

    test("Tuple Load Test") {

        val source = Source.fromFile("./temp/partition1", "ISO8859-1")

        val byteList = source.take(100).toList.map {_.toByte}

        assert(Tuple.fromBytes(byteList).key.value.map(_.toByte) == byteList.take(10))
        assert(Tuple.fromBytes(byteList).value.map(_.toByte) == byteList.drop(10))
    }

    test("Tuple Spec Test 1") {
        val byte_list: List[Byte] = (1 to 110).toList.map {_.toByte}

        assertThrows[IllegalArgumentException]{
            Tuple.fromBytes(byte_list)
        }

    }

    test("Tuple Comparison Test 1") {

        val byteList1: List[Byte] = (1 to 100).toList.map {_.toByte}
        val byteList2: List[Byte] = (2 to 101).toList.map {_.toByte} 

        assert(Tuple.fromBytes(byteList1) < Tuple.fromBytes(byteList2))

    }

    test("Tuple Comparison Test 2") {

        val byteList1: List[Byte] = (1 to 100).toList.map {_.toByte}
        assert(!(Tuple.fromBytes(byteList1) < Tuple.fromBytes(byteList1)))

    }
}