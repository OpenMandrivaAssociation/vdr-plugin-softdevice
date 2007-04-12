
%define plugin	softdevice
%define name	vdr-plugin-%plugin
%define version	0.3.1
%define snapshot 0
%define rel	1
%if %snapshot
%define release	0.%snapshot.%rel
%else
%define release	%rel
%endif

Summary:	VDR plugin: A software emulated MPEG2 device
Name:		%name
Version:	%version
Release:	%mkrel %release
Group:		Video
License:	GPL
URL:		http://softdevice.berlios.de/
%if %snapshot
Source:		vdr-%plugin-%snapshot.tar.bz2
%else
Source:		http://download.berlios.de/softdevice/vdr-%plugin-%version.tar.bz2
%endif
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	vdr-abi = %vdr_abi
BuildRequires:	vdr-devel >= 1.4.1-6
BuildRequires:	ffmpeg-devel
BuildRequires:	libalsa-devel
%if %mdkversion >= 200700
BuildRequires:	dfb++-devel
BuildRequires:	libxv-devel
BuildRequires:	libxinerama-devel
BuildRequires:	dos2unix
%else
BuildRequires:	X11-devel
%endif
Requires(post):	vdr-common

%description
This plugin is a MPEG2 decoder. It can be used as an output device
for the vdr. Possible output devices are Xv, DirectFB, Vidix or a
framebuffer.

%prep
%if %snapshot
%setup -q -n %plugin
%else
%setup -q -n %plugin-%version
%endif
dos2unix CHANGELOG

%vdr_plugin_params_begin %plugin
# See plugin documentation and 'vdr --help' for detailed info
#
# audio output plugin and options
# example: "alsa:mixer"
var=AUDIO_OUT
param='-ao AUDIO_OUT'
# video output plugin and options
# example: "xv:full"
var=VIDEO_OUT
param='-vo VIDEO_OUT'
%vdr_plugin_params_end

%build
# simple configure script
./configure --disable-subplugins
%vdr_plugin_build

%install
rm -rf %{buildroot}
%vdr_plugin_install

%clean
rm -rf %{buildroot}

%post
%{_bindir}/gpasswd -a vdr audio >/dev/null
%vdr_plugin_post %plugin

%postun
%vdr_plugin_postun %plugin

%files -f %plugin.vdr
%defattr(-,root,root)
%doc README HISTORY CHANGELOG

