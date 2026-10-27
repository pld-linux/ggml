# TODO: CUDA bcond, more backends (see below)
#
# Conditional build:
%bcond_without	memkind		# memkind for CPU HBM (64-bit only)
%bcond_without	blas		# BLAS backend
%bcond_without	opencl		# OpenCL backend
%bcond_without	rdma		# RPC backend
%bcond_without	vulkan		# Vulkan backend
# x86 CPU features
%bcond_with	sse42		# SSE 4.2 instructions
%bcond_with	avx		# AVX instructions
%bcond_with	avxvnni		# AVX-VNNI instructions
%bcond_with	avx2		# AVX2 instructions
%bcond_with	bmi2		# BMI2 instructions
%bcond_with	avx512		# AVX512f/AVX512-VBMI/AVX512-VNNI/AVX512-BF16 instructions
%bcond_with	fma		# FMA instructions
%bcond_with	f16c		# F16C instructions
%bcond_with	amx		# AMX-GILE/AMX-INT8/AMX-BF16 instructions
#
%ifnarch %{x8664} ppc64 ppc64le s390x aarch64
%undefine	with_memkind
%endif
Summary:	Tensor library for machine learning
Summary(pl.UTF-8):	Biblioteka tensorów do uczenia maszynowego
Name:		ggml
Version:	0.27.0
Release:	1
License:	MIT
Group:		Libraries
#Source0Download: https://github.com/ggml-org/ggml/releases
Source0:	https://github.com/ggml-org/ggml/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	234a9d5bca089e2ba40a7870b5c5f2f0
URL:		https://github.com/ggml-org/ggml
%{?with_opencl:BuildRequires:	OpenCL-devel}
%{?with_vulkan:BuildRequires:	Vulkan-Loader-devel}
%{?with_blas:BuildRequires:	blas-devel}
BuildRequires:	cmake >= 3.19
BuildRequires:	gcc >= 6:4.7
BuildRequires:	libgomp-devel
%{?with_rdma:BuildRequires:	libibverbs-devel}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
%if %{with opencl}
BuildRequires:	python3 >= 1:3
%endif
# glslc
%{?with_vulkan:BuildRequires:	shaderc}
%{?with_vulkan:BuildRequires:	spirv-headers}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The main goal of ggml is to be a simple, portable, and efficient
tensor library for machine learning with minimal setup.

- Plain C/C++ implementation without any dependencies
- Cross-platform - x86, ARM, RISC-V, LoongArch, PowerPC, s390x, and
  WebAssembly
- SIMD-optimized kernels for x86, ARM, and RISC-V
- Broad backend support - CPU, GPU, NPU, and browser
- 2- to 8-bit integer quantization, plus MXFP4 and NVFP4 microscaling
  formats
- Zero memory allocations during runtime

%description -l pl.UTF-8
Główne założenia ggml to prosta, przenośna i wydajna biblioteka
tensorowa do uczenia maszynowego o minimalnej konfiguracji.

- implementacja w czystym C/C++ bez żadnych zależności
- wieloplatformowa: x86, ARM, RISC-V, LoongArch, PowerPC, s390x,
  WebAssembly
- jądra z optymalizacją SIMD dla x86, ARM, RISC-V
- szeroki zakres backendów: CPU, GPU, NPU oraz przeglądarka
- kwantyzacja od 2 do 8 bitów plus formaty mikroskalowe MXFP4 i NVFP4
- brak przydzielania pamięci w trakcie działania

%package devel
Summary:	Header files for GGML library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki GGML
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for GGML library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki GGML.

%prep
%setup -q

%build
%cmake -B build \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DGGML_BACKEND_DL=ON \
	-DGGML_BACKEND_DIR=%{_libdir}/ggml \
	%{?with_blas:-DGGML_BLAS=ON} \
	%{?with_memkind:-DGGML_CPU_HBM=ON} \
	-DGGML_NATIVE=OFF \
	%{?with_opencl:-DGGML_OPENCL=ON} \
	%{?with_rdma:-DGGML_RPC=ON} \
	%{?with_vulkan:-DGGML_VULKAN=ON} \
	-DGGML_SSE42=%{__ON_OFF sse42} \
	-DGGML_AVX=%{__ON_OFF avx} \
	%{?with_avxvnni:-DGGML_AVX_VNNI=ON} \
	-DGGML_AVX2=%{__ON_OFF avx2} \
	%{?with_avx512:-DGGML_AVX512=ON -DGGML_AVX512_VBMI=ON -DGGML_AVX512_VNNI=ON -DGGML_AVX512_BF16=ON} \
	-DGGML_BMI2=%{__ON_OFF bmi2} \
	%{?with_f16c:-DGGML_F16C=ON} \
	%{?with_fma:-DGGML_FMA=ON} \
	%{?with_amx:-DGGML_AMX_TILE=ON -DGGML_AMX_INT8=ON -DGGML_AMX_BF16=ON}

# -DGGML_CPU_ALL_VARIANTS=ON? (64-bit only? or with patch for ix86 to disable 64-bit only bmi2/avx512+ variants?)
# -DGGML_CUDA on bcond, other GGML_CUDA_* options?
# -DGGML_CANN (BR: Ascend toolkit, aarch64/x86_64 only)
# -DGGML_ET (BR: ET platform)
# -DGGML_HEXAGON* (BR: hexagon SDK)
# -DGGML_HIP* (BR: ROCm toolkit, hip, hipblas, rocblas, ev. rccl)
# -DGGML_MUSA* options? (BR: MUSA toolkit)
# -DGGML_OPENVINO (BR: openvino, aarch64/x86_64 only)
# -DGGML_SYCL* (BR: oneAPI SYCL compiler, ev. oneDNN)
# -DGGML_VIRTGPU* (BR: virglrenderer/venus_hw.h, libdrm-devel) 
# -DGGML_WEBGPU* (BR: Dawn)
# -DGGML_ZDNN (BR: ZDNN library)
# -DGGML_ZENDNN (BR: AMD ZenDNN)

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md docs/gguf.md
%{_libdir}/libggml.so.*.*.*
%ghost %{_libdir}/libggml.so.0
%{_libdir}/libggml-base.so.*.*.*
%ghost %{_libdir}/libggml-base.so.0
%dir %{_libdir}/ggml
# TODO: subpackages for blas, opencl, rpc, vulkan?
%if %{with blas}
%{_libdir}/ggml/libggml-blas.so
%endif
%{_libdir}/ggml/libggml-cpu.so
%if %{with opencl}
%{_libdir}/ggml/libggml-opencl.so
%endif
%if %{with rdma}
%{_libdir}/ggml/libggml-rpc.so
%endif
%if %{with vulkan}
%{_libdir}/ggml/libggml-vulkan.so
%endif

%files devel
%defattr(644,root,root,755)
%{_libdir}/libggml.so
%{_libdir}/libggml-base.so
%{_includedir}/ggml*.h
%{_includedir}/gguf.h
%{_pkgconfigdir}/ggml.pc
%{_libdir}/cmake/ggml
